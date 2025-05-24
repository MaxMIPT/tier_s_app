from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from db_models.workflow_result import WorkflowResult


class WorkflowResultRepository:
    async def create(
            self,
            db: AsyncSession,
            workflow_id: str,
            original_file: str,
            converted_file: Optional[str] = None,
            restored_text: Optional[str] = None,
            voiced_text: Optional[str] = None
    ):
        obj = WorkflowResult(
            workflow_id=workflow_id,
            original_file=original_file,
            converted_file=converted_file,
            restored_text=restored_text,
            voiced_text=voiced_text
        )
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def update(
            self,
            db: AsyncSession,
            workflow_id: str,
            converted_file: Optional[str] = None,
            restored_text: Optional[str] = None,
            voiced_text: Optional[str] = None
    ):
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.workflow_id == workflow_id)
        )
        obj: Optional[WorkflowResult] = result.scalar_one_or_none()
        if obj is None:
            return None
        
        if converted_file is not None:
            obj.converted_file = converted_file
        if restored_text is not None:
            obj.restored_text = restored_text
        if voiced_text is not None:
            obj.voiced_text = voiced_text
        
        await db.commit()
        await db.refresh(obj)
        return obj
    
    async def get(self, db: AsyncSession, workflow_id: str) -> Optional[WorkflowResult]:
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.workflow_id == workflow_id)
        )
        return result.scalar_one_or_none()
    
class WorkflowRepository:
    async def create(self, db: AsyncSession, workflow_id: str, workflow_name: str, task_queue: str) -> None:
        obj = WorkflowResult(workflow_id=workflow_id, workflow_name=workflow_name, task_queue=task_queue)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return

    async def get(self, db: AsyncSession, workflow_id: str) -> Optional[WorkflowResult]:
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.workflow_id == workflow_id)
        )
        return result.scalar_one_or_none()
