from temporalio import activity
from worker.clients.minio_client import minio_client
from services.minio_service import add_new_file, get_file, delete_file
from activities.Model2 import model2


@activity.defn
async def task_3_make_text_better(file_url) -> str:

    # 1. uploads from minio
    old_file = await get_file(minio_client, file_url)

    # 2. run model 2
    ready_file = model2(old_file)

    # 3. upload result of model 2 to minio
    new_file_url = await add_new_file(minio_client, ready_file)

    # 4. delete previous file
    # await delete_file(old_file)

    # 5. add new file's path to the db

    # 6. add status to redis: task 3 is done

    return new_file_url
    # 7. return new file's path
