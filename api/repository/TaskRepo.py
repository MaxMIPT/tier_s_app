from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from db_models.Task import Task
from schemas import TaskModel

class TaskRepository:

    async def insert(self,
                    db: AsyncSession, 
                    taskSchema: TaskModel
                   ) -> None:
        obj = Task(client_id=taskSchema.client_id,
                    workflow_id=taskSchema.workflow_id)
        db.add(obj)
        await db.commit()
    
# -----------------------------------------------------------------------------------

    async def get(self, db: AsyncSession, start_id: int) -> Optional[list[TaskModel]]:
        result = await db.execute(
            select(Task).where(Task.id > start_id)
        )
        orm_result = result.scalars().all()
        return [TaskModel.model_validate(obj) for obj in orm_result]

TaskRepo = TaskRepository()