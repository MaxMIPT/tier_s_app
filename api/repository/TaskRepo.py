import datetime

from typing import Optional
from uuid import UUID

from sqlalchemy import and_, delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Task, Result
from schemas import TaskModel, Task_x_Result


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

    async def get_task_with_result(
        self,
        db: AsyncSession,
        client_id: str,
        workflow_id: Optional[str] = None,
        date_filter: Optional[datetime.datetime] = None,
    ) -> Optional[list[Task_x_Result]]:
        conditions = [Task.client_id == client_id]
        if workflow_id:
            conditions.append(Task.workflow_id == workflow_id)

        if date_filter:
            conditions.append(Task.created_at > date_filter)

        query = (
            select(
                Task.id.label("task_log_id"),
                Task.client_id,
                Task.workflow_id,
                Task.status.label("task_status"),
                Task.created_at,
                Result.original_file,
                Result.original_file_name,
                Result.status.label("status"),
                Result.converted_file,
                Result.converted_file_duration,
                Result.restored_text,
                Result.dubbed_file,
                Result.created_at.label("result_created_at")
            ).select_from(Task).outerjoin(
                Result,
                and_(
                    Task.client_id == Result.client_id,
                    Task.workflow_id == Result.workflow_id
                )
            ).where(and_(*conditions)).order_by(
                Task.created_at.asc()
            )
        )
        try:
            result = await db.execute(query)
            orm_result = result.fetchall()
            return [Task_x_Result.model_validate(arg) for arg in orm_result]
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))

    async def delete(self, db: AsyncSession, workflow_id: UUID) -> None:
        try:
            query = delete(Task).where(Task.workflow_id == workflow_id)
            await db.execute(query)
            await db.commit()
        except SQLAlchemyError as e:
            await db.rollback()
            raise SQLAlchemyError(str(e))
        except Exception as e:
            await db.rollback()
            raise Exception(str(e))
