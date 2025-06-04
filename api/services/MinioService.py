from typing import Any

from aiobotocore.session import ClientCreatorContext
from fastapi import HTTPException, status

from app_logging import logger
from repository import MinioRepository


class MinioService:

    def __init__(self):
        self.repository = MinioRepository()

    async def add_voice_file(
        self, minio_client: ClientCreatorContext, file: Any, filename: str
    ) -> str:
        logger.info(f"Попытка загрузки аудиофайла: {filename}")
        if not file.content_type.startswith("audio/"):
            logger.info(f"Файл отклонён: {filename} — не является аудиофайлом")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Файл не является аудиофайлом",
            )

        file_bytes = await file.read()
        logger.info(f"Размер файла {filename}: {len(file_bytes)} байт")

        file_url = await self.repository.upload_file(
            minio_client=minio_client, file=file_bytes, filename=filename
        )

        logger.info(f"Аудиофайл {filename} успешно загружен: {file_url}")
        return file_url

    async def add_any_file(
        self, minio_client: ClientCreatorContext, file: bytes,
        filename: str, mime_type: str | None = None
    ) -> str:
        logger.info(f"Загрузка произвольного файла: {filename}, MIME: {mime_type}")
        file_url = await self.repository.upload_file(
            minio_client=minio_client, file=file, filename=filename, mime_type=mime_type
        )
        logger.info(f"Файл {filename} успешно загружен: {file_url}")
        return file_url

    async def get_file(
        self, minio_client: ClientCreatorContext, filename: str
    ) -> bytes:
        logger.info(f"Получение файла из MinIO: {filename}")

        file_bytes = await self.repository.get_file(
            minio_client=minio_client, object_name=filename
        )

        logger.info(f"Файл {filename} получен, размер: {len(file_bytes)} байт")
        return file_bytes


minio_service = MinioService()
