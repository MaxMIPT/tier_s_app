import asyncio
from repository.db_repo import WorkflowRepository, WorkflowResultRepository

async def get_new_data(connections, clients, db_client):
    current_id = 1

    while True:
        await asyncio.sleep(5) 
        data_list = await WorkflowResultRepository.get(start_id = current_id, db = db_client)
        current_id += len(data)
        for data in data_list:
            client_id = data.client_id
            for connection_id in clients[client_id]:
                websocket = connections[connection_id]
                status = data.status
                websocket.send_text(status)
                if status == 'success':
                    for connection in clients[client_id]:
                        del connections[connection_id]
                    del clients[client_id]