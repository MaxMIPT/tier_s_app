import asyncio
import uuid

from datetime import datetime
from fastapi import WebSocket, WebSocketDisconnect

from broadcaster import websocket_clients, TaskEventData, TaskEventPing


async def websocket_broadcast_handler(websocket: WebSocket, client_id: str, logger):
    try:
        await websocket.accept()
        client_uuid = client_id
    except Exception:
        await websocket.close()
        return

    channel = asyncio.Queue()
    connection_id = str(uuid.uuid4())
    websocket_clients[connection_id] = {
        "client_id": client_uuid,
        "websocket": websocket,
        "channel": channel,
        "last_time": datetime.now(),
    }

    logger.info(f"Клиент подключён: {client_id}")
    try:
        async def send_loop():
            while True:
                data = await channel.get()
                if isinstance(data, TaskEventData):
                    await websocket.send_json(data.dict())
                elif isinstance(data, TaskEventPing):
                    await websocket.send_bytes(b'ping')

        async def receive_loop():
            while True:
                await websocket.receive_text()

        await asyncio.gather(send_loop(), receive_loop())

    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"Ошибка WebSocket: {e}")
    finally:
        await websocket.close()
        websocket_clients.pop(connection_id, None)
        logger.info(f"Клиент отключён: {client_id}")
