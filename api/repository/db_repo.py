from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Optional

from db_models.workflow_result import WorkflowResult
from db_models.workflow import WorkflowTask
import schemas

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
    
    async def get(self, start_id: int, db: AsyncSession) -> Optional[list[WorkflowResult]]:
        result = await db.execute(
            select(WorkflowResult).where(WorkflowResult.id > start_id)
        )
        orm_result = result.scalars().all()
        return [schemas.WorkflowResultModel.model_validate(obj) for obj in orm_result]

class WorkflowRepository:
    async def create(self, db: AsyncSession, client_id: str, workflow_id: str) -> None:
        obj = WorkflowTask(client_id=client_id, workflow_id=workflow_id)
        db.add(obj)
        await db.commit()
