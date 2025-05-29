from datetime import timedelta
from temporalio import workflow
from activities.convertion_act import task_1_run_convertation
from activities.db_act import insert_to_database
from uuid import UUID
from enum import Enum
from pydantic import BaseModel
from shared import RUN_WORKFLOW_TASK_QUEUE_NAME


import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker")


class StatusEnum(str, Enum):
    success = "success"
    failed = "failed"
    running = "running"


class TaskStatus(str, Enum):
    CREATED = "created"
    AUDIO_CONVERSION_STARTED = "audio_conversion_started"
    AUDIO_CONVERSION_FINISHED = "audio_conversion_finished"
    AUDIO_TRANSCRIPTION_STARTED = "audio_transcription_started"
    AUDIO_TRANSCRIPTION_FINISHED = "audio_transcription_finished"
    AUDIO_DUBBING_STARTED = "audio_dubbing_started"
    AUDIO_DUBBING_FINISHED = "audio_dubbing_finished"
    FINISHED = "finished"
    CANCELED = "canceled"


class WorkflowResultModel(BaseModel):
    workflow_id: UUID
    client_id: str
    original_file: str | None = None
    converted_file: str | None = None
    restored_text: str | None = None
    voiced_text: str | None = None
    status: StatusEnum


class TaskModel(BaseModel):

    client_id: str
    workflow_id: UUID
    status: TaskStatus

    model_config = {"from_attributes": True}


# TODO: сделать класс для отправки статусов на бек
@workflow.defn(name="Workflow")
class Workflow:

    @workflow.run
    async def run(self, file_url: str, client_id: str) -> str:
        info = workflow.info()
        workflow_id = UUID(info.workflow_id)
        try:
            # тут старт воркфлоу
            status_dict = dict(result_data=dict(), task_data=dict())

            # convertion started
            status_dict["task_data"] = TaskModel(
                workflow_id=workflow_id,
                client_id=client_id,
                status=TaskStatus.AUDIO_CONVERSION_STARTED,
            ).model_dump()
            await workflow.execute_activity(
                insert_to_database,
                args=[status_dict["result_data"], status_dict["task_data"]],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )

            # запускаем конвертацию
            file_url_converted = await workflow.execute_activity(
                task_1_run_convertation,
                args=[file_url],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )

            logger.info(f"workflow_id: {workflow_id}")

            # после выполнения (успешное)
            status_dict["task_data"] = TaskModel(
                workflow_id=workflow_id,
                client_id=client_id,
                status=TaskStatus.AUDIO_CONVERSION_FINISHED,
            ).model_dump()
            status_dict["result_data"] = WorkflowResultModel(
                workflow_id=workflow_id,
                client_id=client_id,
                status=StatusEnum.running,
                converted_file=file_url_converted,
            ).model_dump()
            await workflow.execute_activity(
                insert_to_database,
                args=[status_dict["result_data"], status_dict["task_data"]],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )

            # smth else
            # FINISHED
            status_dict["task_data"] = TaskModel(
                workflow_id=workflow_id, client_id=client_id, status=TaskStatus.FINISHED
            ).model_dump()
            status_dict["result_data"] = WorkflowResultModel(
                workflow_id=workflow_id,
                client_id=client_id,
                status=StatusEnum.success,
                converted_file=file_url_converted,
            ).model_dump()
            await workflow.execute_activity(
                insert_to_database,
                args=[status_dict["result_data"], status_dict["task_data"]],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )
            return "макака"

        except Exception as e:
            data = WorkflowResultModel(
                workflow_id=workflow_id, client_id=client_id, status=StatusEnum.failed
            )
            await workflow.execute_activity(
                insert_to_database,
                args=[data.model_dump(), None],
                task_queue=RUN_WORKFLOW_TASK_QUEUE_NAME,
                start_to_close_timeout=timedelta(seconds=60),
            )
            raise e
