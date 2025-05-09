from repository.minio_repo import minio_repo
from fastapi import HTTPException, status

class MinioService:
    async def add_new_file(self,  minio_client, file):
        if not file.content_type.startswith("audio/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Файл не является аудиофайлом")

        file_bytes = await file.read()
        return await minio_repo.upload_file(minio_client, file_bytes)

minio_service = MinioService()