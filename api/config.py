import os
from pydantic import BaseModel
from dotenv import load_dotenv


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


class RedisConfig(BaseModel):
    host: str
    port: int


class Settings(BaseModel):
    db: DBConfig
    minio: MinioConfig
    DATABASE_URL: str


settings = Settings(
    db=DBConfig(
        db_name=os.environ.get("POSTGRES_DB"),
        db_user=os.environ.get("POSTGRES_USER"),
        db_password=os.environ.get("POSTGRES_PASSWORD"),
        db_host=os.environ.get("POSTGRES_HOST"),
        db_port=int(os.environ.get("POSTGRES_PORT")),
    ),
    minio=MinioConfig(
        access_key=os.environ.get("MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("MINIO_SECRET_KEY"),
        bucket_name=os.environ.get("MINIO_BUCKET"),
        endpoint_url=os.environ.get("MINIO_ENDPOINT_URL"),
    ),
    DATABASE_URL=os.environ.get("DATABASE_URL")
)