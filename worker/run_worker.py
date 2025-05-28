import asyncio
from temporalio.client import Client
from temporalio.worker import Worker
import activities
from workflow_def import Workflow

from shared import RUN_WORKFLOW_TASK_QUEUE_NAME

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")

async def main():
    logger.info(msg = 'пробуем запустить клиент')
    client = await Client.connect("temporal:7233",
                                   namespace="default")
    
    logger.info(msg = 'клиент запущен')

    worker = Worker(
        client,
        task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
        debug_mode=True,
        workflows=[Workflow],
        activities=[activities.convertion_act.task_1_run_convertation,
                    activities.db_act.insert_to_database])

    logger.info(msg = 'воркер создан')
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())