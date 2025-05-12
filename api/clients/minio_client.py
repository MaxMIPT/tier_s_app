from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from config import settings

class MinioClient:
    def __init__(
        self, access_key: str, secret_key: str, bucket_name: str, endpoint_url: str
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client


minio_client = MinioClient(
    access_key=settings.minio.access_key,
    secret_key=settings.minio.secret_key,
    bucket_name=settings.minio.bucket_name,
    endpoint_url=settings.minio.endpoint_url,
)
