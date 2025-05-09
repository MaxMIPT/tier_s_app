from repository.minio_repo import minio_repo

class MinioService:
    async def add_new_file(self,  minio_client, file_path):
        await minio_repo.upload_file(minio_client, file_path)

minio_service = MinioService()