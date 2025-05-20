from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine
)
from config import settings
from db_models.workflow import Base

engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
