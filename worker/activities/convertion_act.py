from temporalio import activity
import websockets
import httpx

@activity.defn
async def task_1_run_convertation(file_url) -> str:
    async with websockets.connect("ws://convertion:8002/ws") as ws:
        async with httpx.AsyncClient() as client:
            old_file = await client.get(f"https://app/upload_file/{file_url}")
        await ws.send(old_file.content)
        ready_file = await ws.recv()
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"https://app/download_file/{file_url}", data=ready_file)
        return resp.text
