from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

user = settings.db.db_user
password = settings.db.db_password
db_name = settings.db.db_name
db_port = settings.db.db_port
db_host = settings.db.db_host

DATABASE_URL = f"postgresql+psycopg2://{user}:{password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
