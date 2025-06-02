import asyncio
import logging
import uuid

from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from fastapi import (
    Depends,
    FastAPI,
    File,
    Query,
    Response,
    UploadFile,
    WebSocket,
)
from minio import create_bucket
from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client


from clients import get_db, get_temporal_client, minio_client
from config import settings
from db import init_db
from services import minio_service, workflow_service
from schemas import ResultModel, ResultStatus, TaskModel, TaskStatus


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect(  # noqa
        "temporal:7233", namespace="default"
    )
    await init_db()
    await create_bucket(bucket_name=settings.minio.bucket_name)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/process")
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

    workflow_id = uuid.uuid4()

    await workflow_service.start_workflow(
        temporal_client=client,
        workflow_name="Workflow",
        workflow_id=f"{workflow_id}",
        args=[file_url, client_id],
    )

    await workflow_service.create_task(
        db=db,
        schema=TaskModel(
            client_id=client_id,
            workflow_id=workflow_id,
            status=TaskStatus.CREATED,
        ),
    )

    await workflow_service.create_result(
        db=db,
        schema=ResultModel(
            workflow_id=workflow_id,
            client_id=client_id,
            original_file=file_url,
            status=ResultStatus.running,
        ),
    )


@app.post("/process/stop/{workflow_id}")
async def stop_process_audio(
    workflow_id: uuid.UUID, client: Client = Depends(get_temporal_client)
):
    await workflow_service.stop_workflow(
        temporal_client=client, workflow_id=f"{workflow_id}"
    )


@app.get("/workflows/{client_id}", response_model=List[ResultModel])
async def get_workflow_result(
    client_id: str,
    workflow_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await workflow_service.get_result(
        db=db, client_id=client_id, workflow_id=workflow_id
    )


@app.patch("/workflows")
async def patch_workflow_result(
    payload: ResultModel,
    db: AsyncSession = Depends(get_db),
):
    await workflow_service.update_result(db, payload)


@app.post("/tasks")
async def create_new_task(
    payload: TaskModel,
    db: AsyncSession = Depends(get_db),
):
    await workflow_service.create_task(db, payload)


@app.get("/tasks", response_model=List[TaskModel])
async def get_tasks(
    client_id: str,
    workflow_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    return await workflow_service.get_tasks(
        db, client_id=client_id, workflow_id=workflow_id
    )


@app.get("/files/{path}")
async def download_file(
    path: str, minio_client=Depends(minio_client.get_client)
):
    file = await minio_service.get_file(minio_client, path)
    return Response(
        content=file,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{path}"'},
    )


@app.post("/files")
async def upload_file(
    file: UploadFile = File(...), minio_client=Depends(minio_client.get_client)
):
    file_url = await minio_service.add_any_file(
        minio_client=minio_client, file=file, filename=file.filename
    )
    return file_url


clients = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str):
    await ws.accept()
    connection_id = str(uuid.uuid4())

    if client_id not in clients.keys():
        clients[client_id] = dict()

    clients[client_id][connection_id] = ws
    last_date = datetime.now()
    db_client = await anext(get_db())
    while True:
        await asyncio.sleep(0.2)
        data_list = await workflow_service.get_tasks(
            db=db_client, client_id=client_id, date_filter=last_date
        )

        for data in data_list:
            if not clients[client_id]:
                continue

            for conn, websocket in clients[client_id].items():
                await websocket.send_text(data.json())
                if data.status == "finished":
                    del clients[client_id][conn]

            last_date = data.created_at
