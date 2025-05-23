from aiobotocore.session import ClientCreatorContext
from fastapi import HTTPException, status
from typing import Any

from repository.minio_repo import minio_repo


class MinioService:
    async def add_new_file(
        self, minio_client: ClientCreatorContext,
        file: Any,
        filename: str
    ) -> str:
        if not file.content_type.startswith("audio/"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не является аудиофайлом",
            )

        file_bytes = await file.read()
        return await minio_repo.upload_file(
            minio_client=minio_client,
            file=file_bytes,
            filename=filename
        )


minio_service = MinioService()
