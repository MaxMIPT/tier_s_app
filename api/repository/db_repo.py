from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from db_models.workflow_result import WorkflowResult


class WorkflowResultRepository:
    async def create(
            self,
            db: AsyncSession,
            client_id: str,
            original_file: str,
            converted_file: Optional[str] = None,
            restored_text: Optional[str] = None,
            voiced_text: Optional[str] = None
    ):
        obj = WorkflowResult(
            client_id=client_id,
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
            client_id: str,
            converted_file: Optional[str] = None,
            restored_text: Optional[str] = None,
            voiced_text: Optional[str] = None
    ):
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.client_id == client_id)
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
    
    async def get(self, db: AsyncSession, client_id: str) -> Optional[WorkflowResult]:
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.client_id == client_id)
        )
        return result.scalar_one_or_none()
    
    async def get_workflow_by_client_id(
            db: AsyncSession,
            client_id: str
    ):
        stmt = select(WorkflowResult).where(WorkflowResult.client_id == client_id)
        res = await db.execute(stmt)
        return res.scalar_one_or_none()
    
class WorkflowRepository:
    async def create(self, db: AsyncSession, workflow_name: str, task_queue: str) -> None:
        obj = WorkflowResult(workflow_name=workflow_name, task_queue=task_queue)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return

    async def get(self, db: AsyncSession, client_id: str) -> Optional[WorkflowResult]:
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.client_id == client_id)
        )
        return result.scalar_one_or_none()
