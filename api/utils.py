import asyncio

from datetime import datetime
from clients import get_db
from services import workflow_service

clients = {}
last_dates = {}


async def listen_db():
    db_client = await anext(get_db())
    while True:
        await asyncio.sleep(0.5)

        for client_id, connections in clients.copy().items():
            if client_id not in last_dates.keys():
                last_dates[client_id] = datetime.now()

            last_date = last_dates.get(client_id)
            try:
                data_list = await workflow_service.get_tasks(
                    db=db_client,
                    client_id=client_id,
                    date_filter=last_date
                )
            except Exception:
                continue

            if not data_list:
                continue

            for data in data_list:
                last_dates[client_id] = data.created_at

                for conn_id, websocket in connections.copy().items():
                    try:
                        await websocket.send_text(data.json())
                    except Exception:
                        await websocket.close()
                        del clients[client_id][conn_id]

                    if data.status in ("finished", "canceled"):
                        await websocket.close()
                        del clients[client_id][conn_id]

            if not clients[client_id]:
                del clients[client_id]
                if client_id in last_dates.keys():
                    del last_dates[client_id]
