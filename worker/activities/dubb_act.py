from temporalio import activity

from config import settings


@activity.defn
async def create_audio(text_: str) -> dict:
    from httpx import AsyncClient

    async with AsyncClient() as client:
        audio_response = await client.post(
            f"{settings.AUDIO_API}/audio", params=dict(text_=text_)
        )

    return {"status": "running", "voiced_text": audio_response.json()}
