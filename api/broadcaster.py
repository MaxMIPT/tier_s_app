import asyncio
import uuid

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel
from fastapi.websockets import WebSocket

from services import workflow_service
from clients import get_db

# структура: {client_id: {"websocket": ..., "channel": ..., "last_time": ...}}
websocket_clients: Dict[str, Dict[str, Any]] = {}

class TaskEventItem(BaseModel):
    id: str
    client_id: str
    task_hash: Optional[str] = None
    original_file_url: str
    pipeline_status: str
    task_status: str
    process_converted_file_url: Optional[str] = None
    process_audio_duration_sec: Optional[int] = None
    process_dubbed_file_url: Optional[str] = None
    process_transcripted_text: Optional[str] = None

class TaskEventData(BaseModel):
    task_log_id: int
    task: TaskEventItem
    created_at: str

class TaskEventPing(BaseModel):
    pass

async def broadcast(logger):
    db_client = await anext(get_db())

    while True:
        await asyncio.sleep(0.5)

        for connection_id, client_data in list(websocket_clients.items()):
            last_time: datetime = client_data.get("last_time", datetime.now())
            client_id = client_data.get("client_id", None)
            try:
                data_list = await workflow_service.get_tasks_with_result(
                    db=db_client, client_id=client_id, date_filter=last_time
                )
            except Exception as e:
                logger.error(f"Ошибка получения задач для {client_id}: {e}")
                continue

            for data in data_list:
                task_event = TaskEventData(
                    task_log_id=data.id,
                    created_at=str(data.created_at),
                    task=TaskEventItem(
                        id=str(data.workflow_id),
                        client_id=str(data.client_id),
                        # task_hash=data.task_hash,
                        original_file_url=data.original_file_url,
                        pipeline_status=data.pipeline_status,
                        task_status=data.status,
                        process_converted_file_url=data.process_converted_file_url,
                        # process_audio_duration_sec=data.process_audio_duration_sec,
                        process_dubbed_file_url=data.process_dubbed_file_url,
                        process_transcripted_text=data.process_transcripted_text,
                    )
                )

                await client_data["channel"].put(task_event)
                client_data["last_time"] = data.created_at

async def send_pings():
    while True:
        await asyncio.sleep(10)
        for client_data in websocket_clients.values():
            await client_data["channel"].put(TaskEventPing())

async def stop_broadcast(logger):
    for conn in list(websocket_clients.values()):
        try:
            await conn["websocket"].close()
        except Exception as e:
            logger.error(f"Ошибка при закрытии WebSocket: {e}")
