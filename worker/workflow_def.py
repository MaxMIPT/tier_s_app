import logging

from asyncio import CancelledError
from datetime import timedelta
from typing import Any, List

from temporalio import workflow

from activities import (
    convert_audio,
    create_audio,
    create_text,
    send_task,
    send_result,
)
from config import settings
from schemas import ResultModel, ResultStatus, TaskModel, TaskStatus


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


@workflow.defn(name="Workflow")
class Workflow:

    async def process_task(
        self, workflow_id: str, client_id: str, status: TaskStatus
    ):
        task = TaskModel(
            workflow_id=workflow_id,
            client_id=client_id,
            status=status,
        )
        await workflow.execute_activity(
            send_task,
            args=[task.model_dump()],
            task_queue=settings.RUN_WORKFLOW_TASK_QUEUE_NAME,
            start_to_close_timeout=timedelta(seconds=360),
        )

    async def process_result(self, workflow_id: str, client_id: str, **kwargs):
        result = ResultModel(
            workflow_id=workflow_id, client_id=client_id, **kwargs
        )
        await workflow.execute_activity(
            send_result,
            args=[result.model_dump()],
            task_queue=settings.RUN_WORKFLOW_TASK_QUEUE_NAME,
            start_to_close_timeout=timedelta(seconds=360),
        )

    async def model_activity_wrapper(
        self,
        activity_task,
        args: List[Any],
        workflow_id: str,
        client_id: str,
        input_status: TaskStatus,
        output_status: TaskStatus,
    ) -> Any:
        await self.process_task(
            workflow_id=workflow_id, client_id=client_id, status=input_status
        )
        result = await workflow.execute_activity(
            activity_task,
            args=args,
            task_queue=settings.RUN_WORKFLOW_TASK_QUEUE_NAME,
            start_to_close_timeout=timedelta(seconds=360),
        )
        await workflow.sleep(30)
        await self.process_task(
            workflow_id=workflow_id, client_id=client_id, status=output_status
        )
        await self.process_result(
            workflow_id=workflow_id, client_id=client_id, **result
        )
        return result

    @workflow.run
    async def run(self, file_url: str, client_id: str) -> str:
        info = workflow.info()
        workflow_id = info.workflow_id
        try:
            # convert file format
            convert_task = await self.model_activity_wrapper(
                activity_task=convert_audio,
                args=[file_url],
                workflow_id=workflow_id,
                client_id=client_id,
                input_status=TaskStatus.AUDIO_CONVERSION_STARTED,
                output_status=TaskStatus.AUDIO_CONVERSION_FINISHED,
            )
            converted_file_name = convert_task.get("converted_file")

            # audio to text
            create_text_task = await self.model_activity_wrapper(
                activity_task=create_text,
                args=[converted_file_name],
                workflow_id=workflow_id,
                client_id=client_id,
                input_status=TaskStatus.AUDIO_TRANSCRIPTION_STARTED,
                output_status=TaskStatus.AUDIO_TRANSCRIPTION_FINISHED,
            )
            restored_text = create_text_task.get("restored_text")

            # audio to text
            await self.model_activity_wrapper(
                activity_task=create_audio,
                args=[restored_text],
                workflow_id=workflow_id,
                client_id=client_id,
                input_status=TaskStatus.AUDIO_DUBBING_STARTED,
                output_status=TaskStatus.AUDIO_DUBBING_FINISHED,
            )

            # finished
            await self.process_task(
                workflow_id=workflow_id,
                client_id=client_id,
                status=TaskStatus.FINISHED,
            )
            await self.process_result(
                workflow_id=workflow_id,
                client_id=client_id,
                status=ResultStatus.success,
            )
            return "макака"
        except CancelledError:
            await self.process_task(
                workflow_id=workflow_id,
                client_id=client_id,
                status=TaskStatus.CANCELED,
            )
            await self.process_result(
                workflow_id=workflow_id,
                client_id=client_id,
                status=ResultStatus.failed,
            )
            raise
        except Exception as e:
            await self.process_result(
                workflow_id=workflow_id,
                client_id=client_id,
                status=ResultStatus.failed,
            )
            raise e
