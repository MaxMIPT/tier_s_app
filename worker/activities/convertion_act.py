from asyncio import sleep

from temporalio import activity


@activity.defn
async def task_1_run_convertation(file_url: str) -> str:
    from httpx import AsyncClient

    await sleep(5)
    async with AsyncClient() as client:
        converted_file_name = await client.post(
            "http://convertion:8002/convert", params=dict(file_url=file_url)
        )

    await sleep(5)
    return converted_file_name.text
