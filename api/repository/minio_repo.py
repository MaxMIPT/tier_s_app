from botocore.exceptions import ClientError

class MinioRepository:
    
    def __init__(self):
        self.bucket_name = 'bucket'
        
    async def upload_file(
            self,
            minio_client,
            file_path: str,

    ):
        object_name = file_path.split("/")[-1]
        try:
            async with minio_client as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=object_name,
                        Body=file,
                    )
                print(f"File {object_name} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_file(self, object_name: str, minio_client):
        try:
            async with minio_client as client:
                await client.delete_object(Bucket=self.bucket_name, Key=object_name)
                print(f"File {object_name} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_file(self, object_name: str, destination_path: str, minio_client):
        try:
            async with minio_client as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=object_name)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {object_name} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")

minio_repo = MinioRepository()