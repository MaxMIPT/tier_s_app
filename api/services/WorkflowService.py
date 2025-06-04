import datetime
import uuid

from typing import Any, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from temporalio.client import Client

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
        return await self.result_repo.insert(db, schema)

    async def get_result(
        self,
        db: AsyncSession,
        client_id: str
    ) -> List[ResultModel]:
        return await self.result_repo.get(
            db=db, client_id=client_id
        )

    async def update_result(
        self, db: AsyncSession, schema: UpdateResultModel
    ) -> None:
        await self.result_repo.update(db, schema)
        return

    # Tasks
    async def create_task(self, db: AsyncSession, schema: TaskModel) -> None:
        await self.task_repo.create(db=db, task_schema=schema)
        return

    async def get_tasks(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
        date_filter: Optional[datetime.datetime] = None,
    ):
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
        await self.result_repo.delete(db=db, workflow_id=workflow_id)
        await self.task_repo.delete(db=db, workflow_id=workflow_id)
        await self.workflow_repo.termiate_workflow(
            temporal_client=temporal_client, workflow_id=workflow_id
        )
        return


workflow_service = WorkflowService()
