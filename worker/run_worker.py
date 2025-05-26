import asyncio

from temporalio.client import Client
from temporalio.worker import Worker
import activities
from workflow_def import Workflow
from shared import RUN_WORKFLOW_TASK_QUEUE_NAME
import logging

logger = logging.Logger(name = 'говно')

async def main():
    client = await Client.connect("temporal:7233", namespace="default")
    logger.info(msg = 'клиент запущен')
    worker = Worker(
        client,
        task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
        workflows=[Workflow],
        activities=[activities.convertion_act.task_1_run_convertation,
                    activities.db_act.insert_to_database]
    )
    logger.info(msg = 'воркер создан')
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())