from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, UploadFile, File
from temporalio.client import Client

from clients.temporal_client import get_temporal_client
from clients.minio_client import minio_client
from db import init_db
from services.minio_service import minio_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect("temporal:7233")
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/audio/process")
async def upload_and_process_audio(
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    minio_client=Depends(minio_client.get_client),
):

    file_name = await minio_service.add_new_file(
        minio_client=minio_client,
        file=file,
        filename=file.filename
    )

    await client.start_workflow(
        "TestWorkflow",
        args=[],
        id=f"task_{file_name}",
        task_queue="first-queue"
    )

    return {"file": file_name}
