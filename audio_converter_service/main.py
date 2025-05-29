import model

from fastapi import FastAPI


app = FastAPI()


@app.post("/convert")
async def convert_file(file_url: str):
    # 1. get file original from minio
    # 2. convert file -- model
    # 3. post converted file to minio
    # 4. return file_path converted

    # file = ..  # get file from minio
    file = "aboba"
    return await model.audio_converter(file)
