from temporalio import activity


@activity.defn
async def insert_to_database(result_data: dict = None, task_data: dict = None):
    import httpx  # важно

    # Task
    async with httpx.AsyncClient() as client:
        await client.post("http://api:8000/tasks", json=task_data)

    # Result
    if not result_data:
        return

    async with httpx.AsyncClient() as client:
        await client.patch("http://api:8000/workflows", json=result_data)
