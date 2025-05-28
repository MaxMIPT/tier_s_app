from contextlib import asynccontextmanager
from tempfile import TemporaryDirectory
from uuid import uuid4

from fastapi import (Depends, FastAPI, File, HTTPException, Response,
                     UploadFile, WebSocket, WebSocketDisconnect, status)
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client

import schemas
from clients.db_client import get_db
from clients.minio_client import minio_client
from clients.temporal_client import get_temporal_client
from config import settings
from db import init_db
from db_models.Result import Result  # не удалять!
from db_models.Task import Task  # не удалять!
from minio import create_bucket
from services.MinioService import minio_service
from services.WebsocketService import get_new_data
from services.DbService import dbService
import schemas

RUN_WORKFLOW_TASK_QUEUE_NAME = "RUN_WORKFLOW_TASK"


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.temporal_client = await Client.connect(
        "temporal:7233", namespace="default"
    )

    await init_db()
    db_session = await anext(get_db())
    await get_new_data(connections, clients, db_session)
    await create_bucket(bucket_name=settings.minio.bucket_name)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/audio/process")
async def upload_and_process_audio(
    client_id: str,
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
    db: AsyncSession = Depends(get_db),
):

    file_url = await minio_service.add_any_file(
        minio_client=minio_client, file=file, filename=file.filename
    )
    
    workflow_id = uuid4()

    await client.start_workflow(
        "Workflow",
        args=[file_url, client_id],
        id=f"{workflow_id}",
        task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME
    )

    await dbService.taskInsert(db, client_id = client_id, 
                     workflow_id = workflow_id, status = schemas.TaskStatus.CREATED)
    
    await dbService.resultInsert(db, workflow_id = workflow_id,
                    client_id=client_id,
                    original_file=file_url,
                    status=schemas.ResultStatus.running)


@app.post("/workflow-update-result")
async def create_workflow_results(
    payload: schemas.ResultModel,
    db: AsyncSession = Depends(get_db),
):
    await dbService.resultUpdate(db, payload)


@app.post("/workflow-insert-task")
async def create_workflow_results(
    payload: schemas.TaskModel,
    db: AsyncSession = Depends(get_db),
):
    await dbService.taskInsert(db, payload)


@app.get("/files/{path}")
async def download_file(path:str,
    minio_client=Depends(minio_client.get_client)):
    file = await minio_service.get_file(minio_client, path)
    return Response(
        content=file,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{path}"'},
    )

@app.post("/files") 
async def upload_file(file: UploadFile = File(...),
    minio_client=Depends(minio_client.get_client)):
    file_url = await minio_service.add_any_file(
        minio_client=minio_client, file=file, filename=file.filename
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
