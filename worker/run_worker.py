import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
import activities

import activities.convertion_act
from workflow_def import Workflow
from shared import RUN_WORKFLOW_TASK_QUEUE_NAME

async def main():
    client = await Client.connect("temporal:7233")
    worker = Worker(
        client,
        task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
        workflows=[Workflow],
        activities=[activities.convertion_act.task_1_run_convertation]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())