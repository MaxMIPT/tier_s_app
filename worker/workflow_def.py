from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError
from activities.convertion_act import task_1_run_convertation
import httpx
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

@workflow.defn
class Workflow:

    @workflow.run
    async def run(self, file_url : str, client_id : str) -> str:
        try:
            file_url = await workflow.execute_activity_method(
                task_1_run_convertation, file_url, task_queue = RUN_WORKFLOW_TASK_QUEUE_NAME
            )

            data = WorkflowResultModel(client_id=client_id, status=StatusEnum.running, converted_file=file_url)
            async with httpx.AsyncClient() as client:
                await client.post("http://app:8000/workflow-results", json=data.model_dump())
            return

        except Exception as e:
            data = WorkflowResultModel(client_id=client_id, status=StatusEnum.failed)
            async with httpx.AsyncClient() as client:
                await client.post("http://app:8000/workflow-results", json=data.model_dump())
            raise e