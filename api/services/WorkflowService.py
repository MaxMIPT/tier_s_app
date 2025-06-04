import datetime
import uuid
from typing import Any, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client

from app_logging import logger
from config import settings
from repository import ResultRepository, TaskRepository, TemporalRepository
from schemas import ResultModel, UpdateResultModel, TaskModel


class WorkflowService:

    def __init__(self):
        self.result_repo = ResultRepository()
        self.task_repo = TaskRepository()
        self.workflow_repo = TemporalRepository()

    # Results
    async def create_result(
        self, db: AsyncSession, schema: ResultModel
    ) -> ResultModel | None:
        logger.info(f"Создание результата для workflow_id={schema.workflow_id}")
        return await self.result_repo.insert(db, schema)

    async def get_result(
        self,
        db: AsyncSession,
        client_id: str
    ) -> List[ResultModel]:
        logger.info(f"Получение результатов для client_id={client_id}")
        return await self.result_repo.get(db=db, client_id=client_id)

    async def update_result(
        self, db: AsyncSession, schema: UpdateResultModel
    ) -> None:
        logger.info(f"Обновление результата для workflow_id={schema.workflow_id}")
        await self.result_repo.update(db, schema)
        return

    # Tasks
    async def create_task(self, db: AsyncSession, schema: TaskModel) -> None:
        logger.info(f"Создание задачи для client_id={schema.client_id}, "
                    f"workflow_id={schema.workflow_id}")
        await self.task_repo.create(db=db, task_schema=schema)
        return

    async def get_tasks(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
        date_filter: Optional[datetime.datetime] = None,
    ):
        logger.info(f"Получение задач: client_id={client_id}, "
                    f"workflow_id={workflow_id}, date_filter={date_filter}")
        return await self.task_repo.get(
            db=db,
            client_id=client_id,
            workflow_id=workflow_id,
            date_filter=date_filter,
        )

    async def get_tasks_with_result(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
        date_filter: Optional[datetime.datetime] = None,
    ):
        return await self.task_repo.get_task_with_result(
            db=db,
            client_id=client_id,
            workflow_id=workflow_id,
            date_filter=date_filter,
        )

    # Temporal workflow
    async def start_workflow(
        self,
        temporal_client: Client,
        workflow_name: str,
        workflow_id: uuid.UUID,
        args: list[Any],
    ) -> None:
        logger.info(f"Запуск workflow: {workflow_name}, id={workflow_id}, args={args}")
        await self.workflow_repo.start_workflow(
            temporal_client=temporal_client,
            workflow_name=workflow_name,
            workflow_id=workflow_id,
            args=args,
            task_queue=settings.RUN_WORKFLOW_TASK_QUEUE_NAME,
        )
        return

    async def stop_workflow(
        self,
        temporal_client: Client,
        workflow_id: uuid.UUID,
    ) -> None:
        logger.info(f"Остановка workflow: id={workflow_id}")
        await self.workflow_repo.stop_workflow(
            temporal_client=temporal_client, workflow_id=workflow_id
        )
        return

    async def delete_workflow(
        self,
        db: AsyncSession,
        temporal_client: Client,
        workflow_id: uuid.UUID,
    ) -> None:
        logger.info(f"Удаление workflow: id={workflow_id}")
        await self.result_repo.delete(db=db, workflow_id=workflow_id)
        await self.task_repo.delete(db=db, workflow_id=workflow_id)
        try:
            await self.workflow_repo.termiate_workflow(
                temporal_client=temporal_client, workflow_id=workflow_id
            )
            logger.info(f"Workflow {workflow_id} успешно завершён (terminate)")
        except Exception as e:
            logger.info(f"Ошибка при terminate workflow {workflow_id}: {e}")
        return


workflow_service = WorkflowService()
