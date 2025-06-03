import model

from fastapi import FastAPI
from uuid import uuid4

from file_service import file_service


app = FastAPI()


@app.post("/audio")
async def create_audio(text_: str):
    # 1. convert file -- model
    audio_text: bytes = await model.text_to_audio(text_)
    # 2. post converted file to minio
    audio_text_file_name = await file_service.upload_file(
        file=audio_text, filename=f"final_{uuid4()}.mp4"
    )
    return audio_text_file_name
