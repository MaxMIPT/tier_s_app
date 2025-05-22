import asyncio
from temporalio import activity

@activity.defn
async def _2_convert_to_text(from_1_path) -> str:

    # 1. upload from_1_path from minio
    # 2. run model 1
    # 3. upload result of model 1 to minio
    # 4. delete previous file
    # 5. add new file's path to the db
    # 6. return new file's path
    # 7. add status to redis: task 2 is done
    from_2_path = 'some_path'
    return from_2_path