import asyncio

from api.services.DbService import taskGet
import schemas

async def get_new_data(connections, clients, db_client_generator):
    current_id = 1
    async for db_client in db_client_generator:
        while True:
            await asyncio.sleep(5)
            
            data_list = await taskGet(db_client, current_id)

            current_id += len(data)

            for data in data_list:
                client_id = data.client_id
                for connection_id in clients[client_id]:
                    websocket = connections[connection_id]
                    status = data.status
                    websocket.send_text(status)
                    if status in [schemas.TaskStatus.CANCELED, schemas.TaskStatus.FINISHED]:
                        for connection in clients[client_id]:
                            del connections[connection]
                        del clients[client_id]