import asyncio
import logging

import activities

from temporalio.client import Client
from temporalio.worker import Worker

from config import settings
from workflow_def import Workflow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


async def main():
    logger.info(msg="пробуем запустить клиент")
    client = await Client.connect("temporal:7233", namespace="default")

    logger.info(msg="клиент запущен")

    worker = Worker(
        client,
        task_queue=settings.RUN_WORKFLOW_TASK_QUEUE_NAME,
        debug_mode=True,
        workflows=[Workflow],
        activities=[
            activities.convert_audio,
            activities.create_audio,
            activities.create_text,
            activities.send_task,
            activities.send_result,
        ],
    )

    logger.info(msg="воркер создан")
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
