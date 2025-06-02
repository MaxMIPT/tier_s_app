from temporalio import activity

from schemas import ResultModel, TaskModel


@activity.defn
async def send_task(task_data: TaskModel):
    import httpx  # важно

    async with httpx.AsyncClient() as client:
        await client.post("http://api:8000/tasks", json=task_data.model_dump())


@activity.defn
async def send_result(result_data: ResultModel):
    import httpx

    async with httpx.AsyncClient() as client:
        await client.patch(
            "http://api:8000/workflows", json=result_data.model_dump()
        )
