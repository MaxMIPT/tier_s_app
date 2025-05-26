from sqlalchemy.ext.asyncio import create_async_engine
from config import settings
from sqlalchemy.orm import declarative_base
import logging

logger = logging.Logger(name = 'говно')

engine = create_async_engine(settings.DATABASE_URL, echo=True)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.debug(msg='таблицы типа созданы')
