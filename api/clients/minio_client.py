from contextlib import asynccontextmanager
from aiobotocore.session import get_session

class MinioClient:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": "http://minio:9000"
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

minio_client = MinioClient(access_key='8aKdP5YdSnj9ADcOcMab',
                            secret_key='kzOWWcxOMrAdYoSOj2qBdY8HID95jT2gCpSpVq9O',
                              bucket_name='bucket')

