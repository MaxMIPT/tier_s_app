from uuid import uuid4

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, UploadFile, File, WebSocket
from temporalio.client import Client

from config import settings
from db import init_db
from minio import create_bucket
from redis_client import subscribe

from clients.temporal_client import get_temporal_client
from clients.minio_client import minio_client
from services.minio_service import minio_service


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
    # client_id = 
):
    file_name = await minio_service.add_new_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )

    workflow_id = uuid4()

    # кладем client_id + workflow_id в РЕДИС со статусом задача создана
    # от постгресса (аудита) пока что отказываемся, если успеем - потом прикрутим, ибо это сильно усложняет пайплайн воркфлоу
    
    await client.start_workflow(
        "TestWorkflow",
        args=[file_name, client_id],
        id=f"audio",
        task_queue="first-queue"
    )

    return {"file_name": file_name, "workflow_id": workflow_id}



@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, file_id: str):

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


    await websocket.accept()
    # чтение обновлений от воркфлоу temporal
    async for data in subscribe(file_id):
        # передаем в веб сокет статус
        # (или любой другой объект в текстовом формате)
        await websocket.send_text(str(data))