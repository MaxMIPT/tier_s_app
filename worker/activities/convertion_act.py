from temporalio import activity
import websockets
import httpx

@activity.defn
async def task_1_run_convertation(file_url) -> str:

    try:

        ws = await websockets.connect("ws://convertion:8001/ws")

        async with httpx.AsyncClient() as client:
            old_file = await client.get(f"https://app/upload_file/{file_url}")

        await ws.send(old_file)
        ready_file = await ws.recv()
        
        async with httpx.AsyncClient() as client:
            new_file_url = await client.post(f"https://app/download_file/{file_url}", data=ready_file)

        await ws.close()

        return new_file_url
    
    finally:
        await ws.close()