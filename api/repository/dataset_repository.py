from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db_models.workflow import WorkflowTask


class DatasetRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_file_name(self, file_name: str) -> WorkflowTask | None:
        stmt = select(WorkflowTask).where(WorkflowTask.file_name == file_name)
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()
