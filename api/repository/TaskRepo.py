import datetime

from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from db_models.Task import Task
from schemas import TaskModel


class TaskRepository:

    async def create(self, db: AsyncSession, task_schema: TaskModel) -> None:
        obj = Task(
            client_id=task_schema.client_id,
            workflow_id=task_schema.workflow_id,
            status=task_schema.status,
            created_at=datetime.datetime.now(),
        )
        db.add(obj)
        await db.commit()

    async def get(
        self, db: AsyncSession, client_id: str, date_filter: Optional[datetime.datetime]
    ) -> Optional[list[TaskModel]]:
        conditions = [Task.client_id == client_id]
        if date_filter:
            conditions.append(Task.created_at > date_filter)

        query = select(Task).where(and_(*conditions)).order_by(Task.created_at.asc())

        result = await db.execute(query)
        orm_result = result.scalars().all()
        return [TaskModel.model_validate(obj) for obj in orm_result]
