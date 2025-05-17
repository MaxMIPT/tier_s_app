import json
import time

from temporalio import activity

from redis_client import publish


@activity.defn
async def worker_task(file_name: str) -> str:
    time.sleep(10)
    await publish(
        file_name,
        json.dumps({"my_file_name": file_name, "data": "aboba_1"})
    )
    time.sleep(5)
    await publish(
        file_name,
        json.dumps({"my_file_name": file_name, "data": "aboba_2"})
    )
    return f"ok: {file_name}"
