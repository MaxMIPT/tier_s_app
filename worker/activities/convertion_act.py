from temporalio import activity

from config import settings


@activity.defn
async def convert_audio(file_path: str) -> dict:
    from httpx import AsyncClient

    async with AsyncClient() as client:
        converted_file_name = await client.post(
            f"{settings.CONVERT_API}/convert", params=dict(file_path=file_path)
        )

    return {"status": "running", "converted_file": converted_file_name.json()}
