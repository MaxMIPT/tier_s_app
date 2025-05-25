from fastapi import FastAPI, WebSocket
import httpx

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    url_to_download = await websocket.receive_text()

    async with httpx.AsyncClient() as client:
        resp = await client.get(f"http://app/{url_to_download}")