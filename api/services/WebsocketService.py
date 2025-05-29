import asyncio

import schemas

from services.DbService import dbService


async def get_new_data(connections, clients, db_client):
    current_id = 1
    try:
        while True:
            await asyncio.sleep(5)

            data_list = await dbService.get_tasks(db_client, current_id)  # None
            if data_list:
                current_id += len(data_list)
                for data in data_list:
                    client_id = data.client_id
                    for connection_id in clients[client_id]:
                        websocket = connections[connection_id]
                        status = data.status
                        websocket.send_text(status)
                        if status in [
                            schemas.TaskStatus.CANCELED,
                            schemas.TaskStatus.FINISHED,
                        ]:
                            for connection in clients[client_id]:
                                del connections[connection]
                            del clients[client_id]
    finally:
        await db_client.close()
