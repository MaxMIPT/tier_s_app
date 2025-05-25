import httpx
from temporalio import activity

@activity.defn
async def add_new_line_to_db(data):
    async with httpx.AsyncClient() as client:
        await client.post("https://httpbin.org/get", data=data)