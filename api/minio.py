from aiobotocore.session import get_session

from config import settings


async def create_bucket(bucket_name: str):
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=settings.minio.endpoint_url,
        aws_access_key_id=settings.minio.access_key,
        aws_secret_access_key=settings.minio.secret_key,
    ) as s3:
        try:
            await s3.create_bucket(Bucket=bucket_name)
        except Exception as e:  # noqa
            pass
