from file_repository import HTTPFileRepository


class FileService:

    def __init__(self):
        self.repository = HTTPFileRepository()

    async def get_file(self, filename: str) -> bytes:
        return await self.repository.get_file(filename=filename)


file_service = FileService()
