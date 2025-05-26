from temporalio import activity

@activity.defn
async def task_1_run_convertation(file_url) -> str:
    import websockets # да, именно тут, я не придурок
    import httpx # да, именно тут, я не придурок
    async with websockets.connect("ws://convertion:8002/ws") as ws:
        async with httpx.AsyncClient() as client:
            old_file = await client.get(f"http://api:8000/files/{file_url}")
        await ws.send(old_file.content)
        ready_file = await ws.recv()
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"http://api:8000/files", data=ready_file)
        return resp.text
