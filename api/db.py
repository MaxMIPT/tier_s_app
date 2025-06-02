from sqlalchemy.ext.asyncio import create_async_engine

from config import settings
from db_models import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
