import asyncio
from temporalio import activity

@activity.defn
async def _1_run_convertation(file_url) -> str:

    # 1. upload file from minio
    # 2. convert file
    # 3. upload converted_file to minio
    # 4. delete previous file
    # 5. add new file's path to the db
    # 6. return new file's path
    # 7. add status to redis: task 1 is done
    from_1_path = 'some_path'
    return from_1_path
