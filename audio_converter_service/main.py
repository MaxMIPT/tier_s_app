import model

from fastapi import FastAPI

from file_service import file_service


app = FastAPI()


@app.post("/convert")
async def convert_file(file_path: str):
    # 1. get file original from minio
    file_bytes = await file_service.get_file(filename=file_path)
    # 2. convert file -- model
    file_name = file_path[:file_path.rfind(".")]
    file_extension = file_path[file_path.rfind("."):]

    converted_file: bytes = await model.audio_converter(
        file_bytes=file_bytes,
        file_extension=file_extension
    )
    # 3. post converted file to minio
    converted_file_name = await file_service.upload_file(
        file=converted_file, filename=f"converted_{file_name}.wav"
    )
    return converted_file_name
