import io
import tempfile
import model

from fastapi import FastAPI

from file_service import file_service


app = FastAPI()


@app.post("/text")
async def convert_to_text(file_path: str):
    # 1. get file original from minio
    file_bytes = await file_service.get_file(filename=file_path)
    file_obj = io.BytesIO(file_bytes)

    with tempfile.NamedTemporaryFile(
            suffix=".wav", delete=False) as tmp_input:
        tmp_input.write(file_bytes)
        tmp_input_path = tmp_input.name

    # 2. convert file -- model
    text_from_audio: str = await model.audio_to_text(tmp_input_path)
    return text_from_audio
