from temporalio import activity

from config import settings

@activity.defn
async def convert_audio(file_path: str) -> dict:
    import httpx  # важно

    timeout = httpx.Timeout(
        connect=None,
        read=None,
        write=None,
        pool=None,
    )

    async with httpx.AsyncClient() as client:
        converted_response = await client.post(
            f"{settings.CONVERT_API}/convert", params=dict(file_path=file_path), timeout=timeout
        )
        converted_file = converted_response.json()['filename']
        converted_file_duration = converted_response.json()['duration']

    return {
        "status": "running",
        "converted_file": converted_file,
        "converted_file_duration": converted_file_duration
    }
