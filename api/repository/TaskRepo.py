from sqlalchemy.ext.asyncio import AsyncSession

from db_models.Task import Task

class TaskRepository:
    async def create(self, db: AsyncSession, client_id: str, workflow_id: str) -> None:
        obj = Task(client_id=client_id, workflow_id=workflow_id)
        db.add(obj)
        await db.commit()

workFlowRepo = TaskRepository()