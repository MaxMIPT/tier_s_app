import asyncio
from temporalio import activity

@activity.defn
async def _3_make_text_better(from_1_path) -> str:

    # 1. upload from_2_path from minio
    # 2. run model 3
    # 3. upload result of model 3 to minio
    # 4. delete previous file
    # 5. add new file's path to the db
    # 6. return new file's path
    # 7. add status to redis: task 3 is done
    from_3_path = 'some_path'
    return from_3_path
