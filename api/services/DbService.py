import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from repository.ResultRepo import ResultRepository
from repository.TaskRepo import TaskRepository
from schemas import ResultModel, UpdateResultModel, TaskModel


class DBService:

    def __init__(self):
        self.result_repo = ResultRepository()
        self.task_repo = TaskRepository()

    # Results
    async def create_result(self, db: AsyncSession, schema: ResultModel) -> None:
        await self.result_repo.insert(db, schema)

    async def update_result(self, db: AsyncSession, schema: UpdateResultModel) -> None:
        await self.result_repo.update(db, schema)

    # Tasks
    async def create_task(self, db: AsyncSession, schema: TaskModel) -> None:
        await self.task_repo.create(db=db, task_schema=schema)

    async def get_tasks(
        self, db: AsyncSession, client_id: str, date_filter: Optional[datetime.datetime]
    ):
        return await self.task_repo.get(
            db=db, client_id=client_id, date_filter=date_filter
        )


dbService = DBService()
