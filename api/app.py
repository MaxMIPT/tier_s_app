import asyncio
import datetime

from contextlib import asynccontextmanager
from tempfile import TemporaryDirectory
from uuid import uuid4
import logging

from fastapi import (
    Depends,
    FastAPI,
    File,
    HTTPException,
    Response,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

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


RUN_WORKFLOW_TASK_QUEUE_NAME = "RUN_WORKFLOW_TASK"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.temporal_client = await Client.connect(
        "temporal:7233", namespace="default"
    )

    await init_db()
    # db_session = await anext(get_db())
    # await get_new_data(1, clients, anext(get_db()))
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
        task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
    )

    await dbService.create_task(
        db=db,
        schema=schemas.TaskModel(
            client_id=client_id,
            workflow_id=workflow_id,
            status=schemas.TaskStatus.CREATED,
        ),
    )

    await dbService.create_result(
        db=db,
        schema=schemas.ResultModel(
            workflow_id=workflow_id,
            client_id=client_id,
            original_file=file_url,
            status=schemas.ResultStatus.running,
        ),
    )


@app.patch("/workflows")
async def patch_workflow_result(
    payload: schemas.ResultModel,
    db: AsyncSession = Depends(get_db),
):
    await dbService.update_result(db, payload)


@app.post("/tasks")
async def create_new_task(
    payload: schemas.TaskModel,
    db: AsyncSession = Depends(get_db),
):
    await dbService.create_task(db, payload)


@app.get("/files/{path}")
async def download_file(path: str, minio_client=Depends(minio_client.get_client)):
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


# TODO: сделать клиента
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: str):
    await ws.accept()
    connection_id = str(uuid4())

    if client_id not in clients.keys():
        clients[client_id] = dict()

    clients[client_id][connection_id] = ws
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    async_session_maker = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )
    last_date = None
    while True:
        await asyncio.sleep(5)
        async with async_session_maker() as db_client:
            data_list = await dbService.get_tasks(
                db=db_client, client_id=client_id, date_filter=last_date
            )

        for data in data_list:
            for conn, websocket in clients[client_id].items():
                await websocket.send_text(data.status)
                if data.status == "finished":
                    del clients[client_id][conn]

            last_date = data.created_at
