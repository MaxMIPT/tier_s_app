import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from bar_workflow import TestWorkflow
from foo_activity import worker_task

async def main():
    client = await Client.connect("temporal:7233")
    worker = Worker(
        client,
        task_queue="first-queue",
        workflows=[TestWorkflow],
        activities=[worker_task]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
