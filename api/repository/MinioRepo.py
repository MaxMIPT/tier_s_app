import uuid
from io import BytesIO

from aiobotocore.session import ClientCreatorContext
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from config import settings


class MinioRepository:

    def __init__(self):
        self.bucket_name = settings.minio.bucket_name

    async def upload_file(
        self, minio_client: ClientCreatorContext, file: BytesIO, filename: str
    ) -> str:
        object_name = str(uuid.uuid4()) + "." + filename.split(".")[-1]
        try:
            async with minio_client as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                )
            return object_name

        except ClientError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def get_file(
        self,
        minio_client: ClientCreatorContext,
        object_name: str,
    ) -> bytes:
        try:
            async with minio_client as client:
                response = await client.get_object(
                    Bucket=self.bucket_name, Key=object_name
                )
                data = await response["Body"].read()
                return data
        except ClientError:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


minio_repo = MinioRepository()
