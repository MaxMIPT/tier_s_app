from temporalio import activity
from worker.clients.minio_client import minio_client 
from services.minio_service import add_new_file, get_file, delete_file
from activities.Model3 import model3

@activity.defn
async def task_4_convert_to_voice(file_url) -> str:

    # 1. upload from_1_path from minio
    old_file = await get_file(minio_client, file_url)

    # 2. run model 3
    ready_file = model3(old_file)

    # 3. upload result of model 3 to minio
    new_file_url = await add_new_file(minio_client, ready_file)    

    # 4. delete previous file
    # await delete_file(old_file)

    # 5. add new file's path to the db


    # 6. add status to redis: task 4 is done

    return new_file_url
    # 7. return new file's path