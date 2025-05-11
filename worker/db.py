from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from models import Base

DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base.metadata.create_all(bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session