from temporalio import activity

from config import settings


@activity.defn
async def create_text(file_path: str) -> dict:
    from httpx import AsyncClient

    async with AsyncClient() as client:
        text_response = await client.post(
            f"{settings.TEXT_API}/text", params=dict(file_path=file_path)
        )

    return {"status": "running", "restored_text": text_response.json()}
