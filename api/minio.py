import json

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
            policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "AWS": ["*"]
                        },
                        "Action": ["s3:GetObject"],
                        "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
                    }
                ]
            }
            await s3.put_bucket_policy(
                Bucket=bucket_name,
                Policy=json.dumps(policy)
            )
        except Exception as e:  # noqa
            pass
