import datetime

from typing import Optional

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db_models.task import Task
from schemas import TaskModel


class TaskRepository:

    async def create(self, db: AsyncSession, task_schema: TaskModel) -> None:
        try:
            obj = Task(
                client_id=task_schema.client_id,
                workflow_id=task_schema.workflow_id,
                status=task_schema.status,
                created_at=datetime.datetime.now(),
            )
            db.add(obj)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    async def get(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
        date_filter: Optional[datetime.datetime] = None,
    ) -> Optional[list[TaskModel]]:
        conditions = [Task.client_id == client_id]
        if workflow_id:
            conditions.append(Task.workflow_id == workflow_id)

        if date_filter:
            conditions.append(Task.created_at > date_filter)

        query = (
            select(Task)
            .where(and_(*conditions))
            .order_by(Task.created_at.asc())
        )
        try:
            result = await db.execute(query)
            orm_result = result.scalars().all()
            return [TaskModel.model_validate(obj) for obj in orm_result]
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))
