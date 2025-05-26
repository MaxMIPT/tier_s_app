from fastapi import FastAPI, WebSocket
import model

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    file = model.audio_converter()
    return file