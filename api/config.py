from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()

class DBConfig(BaseModel):
    db_name: str
    db_user: str
    db_password: str
    db_host: str
    db_port: int

class MinioConfig(BaseModel):
    access_key: str
    secret_key: str
    bucket_name: str
    endpoint_url: str

class Settings(BaseModel):
    db: DBConfig
    minio: MinioConfig

settings = Settings(
    db=DBConfig(
        db_name=os.getenv("POSTGRES_DB"),
        db_user=os.getenv("POSTGRES_USER"),
        db_password=os.getenv("POSTGRES_PASSWORD"),
        db_host=os.getenv("POSTGRES_HOST"),
        db_port=os.getenv("POSTGRES_PORT", 5432),
    ),
    minio=MinioConfig(
        access_key=os.getenv("MINIO_ACCESS_KEY"),
        secret_key=os.getenv("MINIO_SECRET_KEY"),
        bucket_name=os.getenv("MINIO_BUCKET"),
        endpoint_url=os.getenv("MINIO_ENDPOINT_URL"),
    ),
)

