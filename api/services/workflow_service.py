# Task 12: Create WorkflowTask entry in DB
from sqlalchemy.ext.asyncio import AsyncSession
from db_models.workflow import WorkflowTask

async def save_workflow_task_to_db(db: AsyncSession, file_name: str, workflow_id: str):
    task = WorkflowTask(file_name=file_name, workflow_id=workflow_id)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
