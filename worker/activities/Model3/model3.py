import asyncio
from temporalio import activity

@activity.defn
async def _4_convert_to_voice(from_1_path) -> str:

    # 1. upload from_3_path from minio
    # 2. run model 4
    # 3. upload result of model 4 to minio
    # 4. delete previous file
    # 5. add new file's path to the db
    # 6. return new file's path
    # 7. add status to redis: task 4 is done
    from_4_path = 'some_path'
    return from_4_path