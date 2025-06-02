from typing import Any

from file_repository import HTTPFileRepository


class FileService:

    def __init__(self):
        self.repository = HTTPFileRepository()

    async def upload_file(self, file: Any, filename: str) -> str:
        # file_bytes = file.read()
        return await self.repository.upload_file(
            file_bytes=file, filename=filename
        )

    async def get_file(self, filename: str) -> bytes:
        return await self.repository.get_file(filename=filename)


file_service = FileService()
