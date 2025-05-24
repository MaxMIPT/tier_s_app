import asyncio
from temporalio import activity
from worker.clients.minio_client import minio_client 
from services.minio_service import add_new_file, get_file, delete_file
from Model1 import model1

@activity.defn
async def _2_convert_to_text(file_url) -> str:

    
    # 1. upload from_1_path from minio
    file_to_model1 = await get_file(minio_client, file_url)
    # 2. run model 1
    ready_file = await model1(file_to_model1)
    # 3. upload result of model 1 to minio
    new_file_url = await add_new_file(ready_file)
    # 4. delete previous file
    delete_file(file_url)
    # 5. add new file's path to the db
    # 6. return new file's path
    # 7. add status to redis: task 2 is done

    return new_file_url