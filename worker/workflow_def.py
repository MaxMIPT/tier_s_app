from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError
from activities.convertion_act import task_1_run_convertation
from activities.db_act import insert_to_database
from enum import Enum
from pydantic import BaseModel
from shared import RUN_WORKFLOW_TASK_QUEUE_NAME


class StatusEnum(str, Enum):
    success = "success"
    failed = "failed"
    running = "running"


class WorkflowResultModel(BaseModel):
    client_id: str
    original_file: str | None
    converted_file: str | None
    restored_text: str | None
    voiced_text: str | None
    status: StatusEnum


@workflow.defn(name="Workflow")
class Workflow:

    @workflow.run
    async def run(self, file_url: str, client_id: str) -> str:
        try:
            # тут старт воркфлоу

            # запускаем активити
            file_url = await workflow.execute_activity(
                task_1_run_convertation,
                args=[file_url],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )
            data = WorkflowResultModel(
                client_id=client_id, status=StatusEnum.running, converted_file=file_url
            )

            # после выполнения (успешное)
            await workflow.execute_activity(
                insert_to_database,
                args=[data.model_dump()],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )
            return 'макака'

        except Exception as e:
            data = WorkflowResultModel(client_id=client_id, status=StatusEnum.failed)
            await workflow.execute_activity(
                insert_to_database,
                args=[data.model_dump()],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )
            raise e
        
            # повторяем для всех остальных тасок