import uuid

from contextlib import asynccontextmanager
from fastapi import (
    Depends,
    FastAPI,
    UploadFile,
    File
)
from sqlalchemy.orm import Session
from temporalio.client import Client

from db import get_db
from utils import get_temporal_client
import db_init

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await Client.connect(
        "temporal:7233"
    )
    yield


app = FastAPI(lifespan=lifespan)

@app.post("/audio/process")
async def upload_and_process_audio(
    file: UploadFile = File(...),
    client: Client = Depends(get_temporal_client),
    db: Session = Depends(get_db)
):
    file_name = str(uuid.uuid4())
    await client.start_workflow(
        "TestWorkflow",
        args=[],
        id=f"task_{file_name}",
        task_queue="first-queue"
    )

    return {"file": file_name}
