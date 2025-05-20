from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)

from config import settings
from db_models.workflow import WorkflowTask


engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


class DatabaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save_workflow_task(self, file_name: str, workflow_id: str):
        task = WorkflowTask(file_name=file_name, workflow_id=workflow_id)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
