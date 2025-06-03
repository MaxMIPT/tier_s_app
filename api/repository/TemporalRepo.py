import uuid

from typing import Any

from fastapi import HTTPException, status
from temporalio.client import Client


class TemporalRepository:

    def __init__(self):
        pass

    async def start_workflow(
        self,
        temporal_client: Client,
        workflow_name: str,
        workflow_id: uuid.UUID,
        args: list[Any],
        task_queue: str,
    ) -> None:
        try:
            await temporal_client.start_workflow(
                workflow_name,
                args=args,
                id=f"{workflow_id}",
                task_queue=task_queue,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
            )

    async def stop_workflow(
        self, temporal_client: Client, workflow_id: uuid.UUID
    ) -> None:
        try:
            await temporal_client.get_workflow_handle(
                workflow_id=f"{workflow_id}"
            ).cancel()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
            )

    async def termiate_workflow(
        self, temporal_client: Client, workflow_id: uuid.UUID
    ) -> None:
        try:
            await temporal_client.get_workflow_handle(
                workflow_id=f"{workflow_id}"
            ).terminate(reason="Terminated by User.")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=e
            )
