from temporalio import activity
from worker.clients.minio_client import minio_client 
from services.minio_service import add_new_file, get_file, delete_file
from activities.Convert import convert

@activity.defn
async def task_2_convert_to_text(file_url) -> str:

    # 1. upload from_1_path from minio
    old_file = await get_file(minio_client, file_url)

    # 2. run model 1
    ready_file = convert(old_file)

    # 3. upload result of model 1 to minio
    new_file_url = await add_new_file(minio_client, ready_file)    

    # 4. delete previous file
    #await delete_file(old_file)

    # 5. add new file's path to the db
    

    # 6. add status to redis: task 2 is done

    return new_file_url
    # 7. return new file's path