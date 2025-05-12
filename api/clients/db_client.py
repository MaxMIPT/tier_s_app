from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import settings
from models import Base

user = settings.db.db_user
password = settings.db.db_password
db_name = settings.db.db_name
db_port = settings.db.db_port
db_host = settings.db.db_host

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{db_host}:{db_port}/{db_name}"

engine = create_async_engine(DATABASE_URL)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base.metadata.create_all(bind=engine)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
