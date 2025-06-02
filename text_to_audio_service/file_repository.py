from httpx import AsyncClient

from config import settings


class HTTPFileRepository:

    async def upload_file(self, file_bytes: bytes, filename: str) -> str:
        async with AsyncClient() as client:
            files = {
                "file": (filename, file_bytes, "application/octet-stream")
            }
            response = await client.post(
                f"{settings.API_URL}/files", files=files
            )
            return response.json()
