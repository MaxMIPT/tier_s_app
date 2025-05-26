from tempfile import TemporaryDirectory
from uuid import uuid4

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, UploadFile, File, WebSocket, HTTPException, WebSocketDisconnect, status
from fastapi.responses import FileResponse
from temporalio.client import Client
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from clients.db_client import get_db
from clients.minio_client import minio_client
from repository.db_repo import workFlowRepo, workFlowResultRepo

from db import init_db
from db_models.workflow_result import WorkflowResult # не удалять!
from db_models.workflow import WorkflowTask # не удалять!

from minio import create_bucket
from clients.temporal_client import get_temporal_client
from clients.minio_client import minio_client
from services.minio_service import minio_service
from services.websocket_data import get_new_data
import schemas
import asyncio

RUN_WORKFLOW_TASK_QUEUE_NAME = "WORKFLOW_TASK_QUEUE"

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.temporal_client = await Client.connect("temporal:7233", namespace="default")
    await init_db()
    await create_bucket(bucket_name=settings.minio.bucket_name)
    #asyncio.create_task(get_new_data(connections, clients, get_db()))
    yield

#----------------------------------------------------------------------------------------

app = FastAPI(lifespan=lifespan)

@app.post("/audio/process")
async def upload_and_process_audio(
    client_id: str,
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
    db: AsyncSession = Depends(get_db),
):
    file_url = await minio_service.add_new_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )

    workflow_id = uuid4()
    
    await client.start_workflow(
        "Workflow",
        args=[file_url, client_id],
        id=workflow_id,
        task_queue="RUN_WORKFLOW_TASK_QUEUE_NAME"
    )

    payload = schemas.WorkflowModel(workflow_id = workflow_id, client_id = client_id)
    
    obj = await workFlowRepo.create(db = db, **payload.model_dump())
    await db.commit()
    await db.refresh(obj)
    return obj

@app.post("/workflow-results")
async def create_workflow_results(
    payload: schemas.WorkflowResultModel,
    db: AsyncSession = Depends(get_db),
):
    obj = await workFlowResultRepo.create(db = db, 
                            **payload.model_dump())
    if not obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create workflow result")

@app.get("/upload_file/{path}")
async def download_files(path:str, 
                         minio_client=Depends(minio_client.get_client)):
    file = await minio_service.get_file(minio_client, path)
    return file

@app.get("/download_file/")
async def download_files(file: UploadFile = File(...),
                          minio_client=Depends(minio_client.get_client)):
    file_url = await minio_service.add_any_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )
    return file_url

connections = {}
clients = {}

@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connection_id = str(uuid4())

    try:
        init_msg = await ws.receive_json()
        if init_msg.get("message_type") != "set_client_id":
            await ws.close(code=400)
            return

        connections[connection_id] = ws
        client_id = init_msg.get("client_id")
        clients.setdefault(client_id, []).append(connection_id)

    finally:
        del connections[connection_id]
        clients[client_id].remove(connection_id)