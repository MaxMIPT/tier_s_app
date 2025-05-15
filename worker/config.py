import os

from pydantic import BaseModel


class MinioConfig(BaseModel):
    access_key: str
    secret_key: str
    bucket_name: str
    endpoint_url: str


class RedisConfig(BaseModel):
    host: str
    port: int


class Settings(BaseModel):
    minio: MinioConfig
    redis: RedisConfig
    DATABASE_URL: str


settings = Settings(
    minio=MinioConfig(
        access_key=os.environ.get("MINIO_ACCESS_KEY"),
        secret_key=os.environ.get("MINIO_SECRET_KEY"),
        bucket_name=os.environ.get("MINIO_BUCKET"),
        endpoint_url=os.environ.get("MINIO_ENDPOINT_URL"),
    ),
    redis=RedisConfig(
        host=os.environ.get("REDIS_HOST"),
        port=int(os.environ.get("REDIS_PORT"))
    ),
    DATABASE_URL=os.environ.get("DATABASE_URL")
)
