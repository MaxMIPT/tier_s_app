import os
import subprocess
import tempfile

from temporalio import activity

from config import settings
from clients.minio_client import minio_client
from services.redis_service import publish_message


@activity.defn
async def convert_audio(file_name: str, workflow_id: str) -> str:
    tmp_dir = tempfile.mkdtemp()
    src_path = os.path.join(tmp_dir, file_name)

    ext = os.path.splitext(file_name)[1].lower()
    if ext != ".wav":
        out_name = os.path.splitext(file_name)[0] + ".wav"
        out_path = os.path.join(tmp_dir, out_name)
        subprocess.run(["ffmpeg", "-y", "-i", src_path, out_path], check=True)
    else:
        out_name = file_name
        out_path = src_path

    async with await minio_client.get_client() as client:
        bucket = settings.minio.bucket_name
        with open(out_path, "rb") as f:
            await client.put_object(Bucket=bucket, Key=out_name, Body=f.read())

    await publish_message(f"workflow-{workflow_id}", out_name)

    return out_name
