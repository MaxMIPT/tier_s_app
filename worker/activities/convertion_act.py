from temporalio import activity
from worker.clients.minio_client import minio_client 
from services.minio_service import add_new_file, get_file
import websockets

@activity.defn
async def task_1_run_convertation(file_url) -> str:

    try:
        old_file = await get_file(minio_client, file_url)

        ws = await websockets.connect("ws://convetion:8001/ws")

        await ws.send(old_file)
        ready_file = await ws.recv()
        
        new_file_url = await add_new_file(minio_client, ready_file)
        await ws.close()
        return new_file_url
    finally:
        await ws.close()