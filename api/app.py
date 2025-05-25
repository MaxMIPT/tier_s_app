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
from repository.db_repo import WorkflowRepository, WorkflowResultRepository
from db import init_db
from minio import create_bucket
from asyncio import create_task
from clients.temporal_client import get_temporal_client
from clients.minio_client import minio_client
from services.minio_service import minio_service
from json import loads
from pydantic import BaseModel
from enum import Enum
import loguru

import time

class StatusEnum(str, Enum):
    success = "success"
    failed = "failed"
    running = "running"
    
class WorkflowResultModel(BaseModel):
    client_id: str
    original_file: str
    converted_file: str
    restored_text: str
    voiced_text: str
    status: StatusEnum

class WorkflowModel(BaseModel):
    file_id: str
    workflow_id: str

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
    # create_task(redis_listener())
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/audio/process")
async def upload_and_process_audio(
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
    # client_id = 
):
    file_name = await minio_service.add_new_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )

    workflow_id = uuid4()
    
    await client.start_workflow(
        "TestWorkflow",
        # args=[file_name, client_id],
        id=f"audio",
        task_queue="first-queue"
    )

    return {"file_name": file_name, "workflow_id": workflow_id}

@app.post("/workflows")
async def create_workflow(
    payload: WorkflowModel,
    db: AsyncSession = Depends(get_db()),
):
    repo = WorkflowRepository()
    obj = await repo.create(db = db, **payload.model_dump())
    await db.commit()
    await db.refresh(obj)
    return obj

@app.post("/workflow-results")
async def create_workflow_results(
    payload: WorkflowResultModel,
    db: AsyncSession = Depends(get_db()),
):
    repo = WorkflowResultRepository()
    obj = await repo.create(db = db, **payload.model_dump())
    if not obj:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create workflow result")
    return obj

@app.get("/download_files")
async def download_files(path:str):
    client = minio_client.get_client()
    bucket = settings.minio.bucket_name
    try:
        obj = await client.get_object(bucket, path)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    
    filename = path.split("/")[-1]
    tmp_dir = TemporaryDirectory()
    dst = tmp_dir.name + "/" + filename
    with open(dst, "wb") as f:
        async for chunk in obj:
            f.write(chunk)
    return FileResponse(path=dst, filename=filename, media_type="application/octet-stream")



# connections = {}
# clients = {}

# @app.websocket("/ws")
# async def websocket_endpoint(ws: WebSocket):
    
#     await ws.accept()

#     session = AsyncSession()
#     connection_id = str(uuid4())
#     client_id = None

#     try:
#         init_msg = await ws.receive_json()
#         if init_msg.get("message_type") != "set_client_id":
#             await ws.close(code=400)
#             return
        
#         client_id = init_msg.get("client_id")
#         connection_id = init_msg.get("connection_id", connection_id)

#         connections[connection_id] = client_id
#         clients.setdefault(client_id, set()).add(connection_id)

#         await ws.send_json(
#             {
#                 "message_type": "connection_ack",
#                 "client_id": client_id,
#                 "connection_id": connection_id
#             }
#         )

#         while True:
#             msg = await ws.receive_json()
#             msg_type = msg.get("message_type")
#     except WebSocketDisconnect:
#         pass
    

    
    # сокет создаем общий ДЛЯ ВСЕХ
    # при подключении клиент браузера АВТОМАТИЧЕСКИ присылает свой connection_id
    # здесь его надо добавить в мапу коннекшином и следить за тем, что когда коннекшин оборвался -> удалять его из мапы
    # как это сделать тут точно хз, обычно можно прямо для коннекшина задать событие которые выполнится после разрыва соединения

    # процесс чтения сообщения запускается в самом начале фрейморком, куда приходит АВТОМАТИЧЕСКИ connection_id
    # когда приходит сообщение с message_type=set_client_id, мы в мапу сооединение добавляем информацию о том, что к этому connection_id относится этот client_id

    # map[connection_id] => client_id
    # map[client_id] => []connection_id

    # ---- ПАРАЛЕЛЬНО
    # читаем нашу шину данных, из которой приходят сообщения, содержищие client_id, worflow_id, task_type и data
    # когда пришло такое сообщение, ищем соединения (массив connection_id) принадлежащих этому client_id
    # если массив не пустой, каждому connection_id из массива отправляем сообщение со стороны сервера: {message_type:workflow_update, workflow_id: workflow_id, task_type: task_type, data: data}