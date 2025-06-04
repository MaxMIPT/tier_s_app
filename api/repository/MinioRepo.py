import uuid

from aiobotocore.session import ClientCreatorContext
from botocore.exceptions import ClientError
from fastapi import HTTPException, status

from config import settings
import magic


class MinioRepository:

    def __init__(self):
        self.bucket_name = settings.minio.bucket_name
        self._mime_detector = magic.Magic(mime=True)

    async def upload_file(
        self, minio_client: ClientCreatorContext, file: bytes, filename: str, mime_type: str | None = None
    ) -> str:
        ext = f".{filename.split('.')[-1]}"

        if mime_type is None:
            mime_type = self._mime_detector.from_buffer(file)

            if mime_type is None:
                mime_type = "application/octet-stream"

        object_name = str(uuid.uuid4()) + ext

        try:
            async with minio_client as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=object_name,
                    Body=file,
                    ContentType=mime_type,
                )
            return object_name

        except ClientError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
