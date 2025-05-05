from temporalio import activity


@activity.defn
async def worker_task() -> str:
    print('Worker task started')
    # do smth
    return "ok"
