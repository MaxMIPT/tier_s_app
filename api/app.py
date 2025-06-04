import asyncio
import uuid

from contextlib import asynccontextmanager
from typing import List, Optional

from fastapi import (
    Depends,
    FastAPI,
    File,
    Query,
    Response,
    UploadFile,
    WebSocket,
    HTTPException,
    status
)
from minio import create_bucket
from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client

from fastapi.middleware.cors import CORSMiddleware


from app_logging import setup_logger, logging
from clients import get_db, get_temporal_client, minio_client
from config import settings
from db import init_db
from services import minio_service, workflow_service
from schemas import ResultModel, ResultStatus, TaskModel, TaskStatus

from broadcaster import broadcast, send_pings, stop_broadcast
from websocket_broadcast import websocket_broadcast_handler

import magic
mime_detector = magic.Magic(mime=True)

setup_logger()

logger = logging.getLogger("websocket")
logger.setLevel(logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect(  # noqa
        "temporal:7233", namespace="default"
    )
    await init_db()
    await create_bucket(bucket_name=settings.minio.bucket_name)
    asyncio.create_task(broadcast(logger))
    asyncio.create_task(send_pings())
    yield
    await stop_broadcast(logger)


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)


@app.post("/process", response_model=ResultModel)
async def upload_and_process_audio(
    client_id: str,
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
    db: AsyncSession = Depends(get_db),
):
    file_bytes = await file.read()
    mime_type = mime_detector.from_buffer(file_bytes)
    if mime_type is None or not mime_type.startswith("audio/"):
        if mime_type == "video/webm" and file.content_type == "audio/webm":
            mime_type = "audio/webm"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ожидается аудиофайл, получен: {mime_type or 'неизвестный формат'}",
            )

    file_url = await minio_service.add_any_file(
        minio_client=minio_client,
        file=file_bytes,
        filename=file.filename,
        mime_type=mime_type
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

    result = await workflow_service.create_result(
        db=db,
        schema=ResultModel(
            workflow_id=workflow_id,
            client_id=client_id,
            original_file=file_url,
            status=ResultStatus.running,
        ),
    )
    return result


@app.post("/process/stop/{workflow_id}")
async def stop_process_audio(
    workflow_id: uuid.UUID, client: Client = Depends(get_temporal_client)
):
    await workflow_service.stop_workflow(
        temporal_client=client, workflow_id=f"{workflow_id}"
    )


@app.delete("/process/{workflow_id}")
async def delete_process_audio(
    workflow_id: uuid.UUID,
    client: Client = Depends(get_temporal_client),
    db: AsyncSession = Depends(get_db),
):
    await workflow_service.delete_workflow(
        db=db, temporal_client=client, workflow_id=f"{workflow_id}"
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
    file_bytes = await file.read()
    file_url = await minio_service.add_any_file(
        minio_client=minio_client, file=file_bytes, filename=file.filename
    )
    return file_url


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket_broadcast_handler(websocket, client_id, logger)
