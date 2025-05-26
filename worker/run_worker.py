import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
import activities

import activities.convertion_act
from workflow_def import Workflow

RUN_WORKFLOW_TASK_QUEUE_NAME = "WORKFLOW_TASK_QUEUE"

async def main():
    client = await Client.connect("temporal:7233")
    worker = Worker(
        client,
        task_queue="WORKFLOW_TASK_QUEUE-queue",
        workflows=[Workflow],
        activities=[activities.convertion_act]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())