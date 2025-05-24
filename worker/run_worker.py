import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
import activities

import activities.Convert
import activities.Convert.convert
import activities.Convert.step1
from worker.workflow_def import TestWorkflow

RUN_WORKFLOW_TASK_QUEUE_NAME = "WORKFLOW_TASK_QUEUE"

async def main():
    client = await Client.connect("temporal:7233")
    worker = Worker(
        client,
        task_queue="WORKFLOW_TASK_QUEUE-queue",
        workflows=[TestWorkflow],
        activities=[activities.Convert.step1.task_1_run_convertation,
                    activities.Model1.step2.task_2_convert_to_text,
                    activities.Model2.step3.task_3_make_text_better,
                    activities.Model3.step4.task_4_convert_to_voice]
    )
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())