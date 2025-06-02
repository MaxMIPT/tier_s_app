from typing import Any

from aiobotocore.session import ClientCreatorContext
from fastapi import HTTPException, status

from repository import MinioRepository


class MinioService:

    def __init__(self):
        self.repository = MinioRepository()

    async def add_voice_file(
        self, minio_client: ClientCreatorContext, file: Any, filename: str
    ) -> str:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не является аудиофайлом",
            )

        file_bytes = await file.read()
        return await self.repository.upload_file(
            minio_client=minio_client, file=file_bytes, filename=filename
        )

    async def add_any_file(
        self, minio_client: ClientCreatorContext, file: Any, filename: str
    ) -> str:

        file_bytes = await file.read()
        return await self.repository.upload_file(
            minio_client=minio_client, file=file_bytes, filename=filename
        )

    async def get_file(
        self, minio_client: ClientCreatorContext, filename: str
    ) -> bytes:

        return await self.repository.get_file(
            minio_client=minio_client, object_name=filename
        )


minio_service = MinioService()
