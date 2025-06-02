import model

from fastapi import FastAPI
from uuid import uuid4

from file_service import file_service


app = FastAPI()


@app.post("/convert")
async def convert_file(file_path: str):
    # 1. get file original from minio
    file_bytes = await file_service.get_file(filename=file_path)
    # 2. convert file -- model
    converted_file: bytes = await model.audio_converter(file_bytes)
    # 3. post converted file to minio
    converted_file_name = await file_service.upload_file(
        file=converted_file, filename=f"converted_{uuid4()}.mp4"
    )
    return converted_file_name
