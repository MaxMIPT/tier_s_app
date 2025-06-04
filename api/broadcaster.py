import asyncio
import uuid

from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field

from services import workflow_service
from clients import get_db

# структура: {client_id: {"websocket": ..., "channel": ..., "last_time": ...}}
websocket_clients: Dict[str, Dict[str, Any]] = {}


class ResultEventData(BaseModel):
    workflow_id: str
    client_id: str
    original_file: str | None = Field(None)
    original_file_name: str | None = Field(None)
    converted_file: str | None = Field(None)
    converted_file_duration: float | None = Field(None)
    restored_text: str | None = Field(None)
    dubbed_file: str | None = Field(None)
    status: str
    task_status: str | None = Field(None)
    created_at: str


class TaskEventData(BaseModel):
    task_log_id: int
    workflow: ResultEventData
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
                    task_log_id=data.task_log_id,
                    created_at=str(data.created_at),
                    workflow=ResultEventData(
                        workflow_id=str(data.workflow_id),
                        client_id=str(data.client_id),
                        original_file=data.original_file,
                        original_file_name=data.original_file_name,
                        converted_file=data.converted_file,
                        converted_file_duration=data.converted_file_duration,
                        restored_text=data.restored_text,
                        dubbed_file=data.dubbed_file,
                        status=data.status,
                        task_status=data.task_status,
                        created_at=str(data.result_created_at)
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
