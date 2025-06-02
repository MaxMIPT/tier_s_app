from httpx import AsyncClient

from config import settings


class HTTPFileRepository:

    async def get_file(self, filename: str) -> bytes:
        async with AsyncClient() as client:
            response = await client.get(f"{settings.API_URL}/files/{filename}")
            return response.content
