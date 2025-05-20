from uuid import uuid4

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, UploadFile, File, WebSocket
from temporalio.client import Client

from config import settings
from db import init_db, get_db
from minio import create_bucket
from redis_client import subscribe

from clients.temporal_client import get_temporal_client
from clients.minio_client import minio_client
from services.minio_service import minio_service

from sqlalchemy.ext.asyncio import AsyncSession
from services.workflow_service import save_workflow_task_to_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Выполняется перед запуском API приложения
    :param app:
    :return:
    """
    # подрубаемся к темпоралу
    app.state.temporal_client = await Client.connect("temporal:7233")
    # инициализация схемы БД
    await init_db()
    # создаем бакет в minio для хранения файлов
    await create_bucket(bucket_name=settings.minio.bucket_name)
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/audio/process")
async def upload_and_process_audio(
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
    db: AsyncSession = Depends(get_db) 
):
    file_name = await minio_service.add_new_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )

    workflow_id = uuid4()
    await client.start_workflow(
        "TestWorkflow",
        args=[file_name],
        id=f"audio_{workflow_id}",
        task_queue="first-queue"
    )
    
    await save_workflow_task_to_db(db=db, file_name=file_name, workflow_id=str(workflow_id))

    return {"file_name": file_name, "workflow_id": workflow_id}


@app.websocket("/ws/{file_id}")
async def websocket_endpoint(websocket: WebSocket, file_id: str):
    await websocket.accept()
    # чтение обновлений от воркфлоу temporal
    async for data in subscribe(file_id):
        # передаем в веб сокет статус
        # (или любой другой объект в текстовом формате)
        await websocket.send_text(str(data))
