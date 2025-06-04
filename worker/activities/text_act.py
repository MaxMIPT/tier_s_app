from temporalio import activity

from config import settings


@activity.defn
async def create_text(file_path: str) -> dict:
    import httpx

    timeout = httpx.Timeout(
        connect=None,
        read=None,
        write=None,
        pool=None,
    )

    async with httpx.AsyncClient() as client:
        text_response = await client.post(
            f"{settings.TEXT_API}/text", params=dict(file_path=file_path), timeout=timeout
        )

    return {"status": "running", "restored_text": text_response.json()}
