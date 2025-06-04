from temporalio import activity

from config import settings


@activity.defn
async def create_audio(text_: str) -> dict:
    import httpx

    timeout = httpx.Timeout(
        connect=None,
        read=None,
        write=None,
        pool=None,
    )

    async with httpx.AsyncClient() as client:
        audio_response = await client.post(
            f"{settings.AUDIO_API}/audio", params=dict(text_=text_), timeout=timeout
        )

    return {"status": "running", "dubbed_file": audio_response.json()}
