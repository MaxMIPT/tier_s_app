from temporalio import activity

@activity.defn
async def insert_to_database(data):
    import httpx # да, именно тут, я не придурок
    async with httpx.AsyncClient() as client:
        await client.post("http://app:8000/workflow-results", json=data)