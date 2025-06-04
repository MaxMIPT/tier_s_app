from temporalio import activity

from schemas import ResultModel, TaskModel


@activity.defn
async def send_task(task_data: TaskModel):
    import httpx  # важно

    timeout = httpx.Timeout(
        connect=None,
        read=None,
        write=None,
        pool=None,
    )

    async with httpx.AsyncClient() as client:
        await client.post("http://api:8000/tasks", json=task_data.model_dump(), timeout=timeout)


@activity.defn
async def send_result(result_data: ResultModel):
    import httpx

    timeout = httpx.Timeout(
        connect=None,
        read=None,
        write=None,
        pool=None,
    )

    async with httpx.AsyncClient() as client:
        await client.patch(
            "http://api:8000/workflows", json=result_data.model_dump(), timeout=timeout
        )
