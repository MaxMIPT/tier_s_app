import uuid
from typing import Any

from fastapi import HTTPException, status
from temporalio.client import Client

from app_logging import logger


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
        logger.info(f"Запуск workflow: name={workflow_name}, "
                    f"id={workflow_id}, queue={task_queue}, args={args}")
        try:
            await temporal_client.start_workflow(
                workflow_name,
                args=args,
                id=str(workflow_id),
                task_queue=task_queue,
            )
            logger.info(f"Workflow {workflow_id} успешно запущен")
        except Exception as e:
            logger.error(f"Ошибка запуска workflow {workflow_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def stop_workflow(
        self, temporal_client: Client, workflow_id: uuid.UUID
    ) -> None:
        logger.info(f"Остановка workflow: id={workflow_id}")
        try:
            await temporal_client.get_workflow_handle(str(workflow_id)).cancel()
            logger.info(f"Workflow {workflow_id} успешно остановлен")
        except Exception as e:
            logger.error(f"Ошибка остановки workflow {workflow_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    async def termiate_workflow(
        self, temporal_client: Client, workflow_id: uuid.UUID
    ) -> None:
        logger.info(f"Принудительное завершение workflow: id={workflow_id}")
        try:
            await temporal_client.get_workflow_handle(str(workflow_id)).terminate(
                reason="Terminated by User."
            )
            logger.info(f"Workflow {workflow_id} успешно завершён")
        except Exception as e:
            logger.error(f"Ошибка завершения workflow {workflow_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
