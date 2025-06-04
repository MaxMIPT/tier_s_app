import datetime

from uuid import UUID

from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional


class BaseSchema(BaseModel):

    model_config = {"from_attributes": True}


class ResultStatus(str, Enum):
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


class ResultModel(BaseSchema):
    workflow_id: UUID | None
    client_id: str
    original_file: str | None = Field(None)
    original_file_name: str | None = Field(None)
    converted_file: str | None = Field(None)
    converted_file_duration: float | None = Field(None)
    restored_text: str | None = Field(None)
    dubbed_file: str | None = Field(None)
    status: ResultStatus
    task_status: TaskStatus | None = Field(None)
    created_at: datetime.datetime = datetime.datetime.now()


class UpdateResultModel(BaseSchema):
    workflow_id: UUID
    status: ResultStatus
    converted_file: Optional[str] = (None,)
    converted_file_duration: Optional[float] = (None,)
    restored_text: Optional[str] = (None,)
    dubbed_file: Optional[str] = None


class TaskModel(BaseSchema):
    client_id: str
    workflow_id: UUID
    status: TaskStatus
    created_at: datetime.datetime = datetime.datetime.now()


class Task_x_Result(BaseSchema):
    task_log_id: int
    workflow_id: UUID | None
    client_id: str
    original_file: str | None = Field(None)
    original_file_name: str | None = Field(None)
    converted_file: str | None = Field(None)
    converted_file_duration: float | None = Field(None)
    restored_text: str | None = Field(None)
    dubbed_file: str | None = Field(None)
    status: ResultStatus
    task_status: TaskStatus | None = Field(None)
    result_created_at: datetime.datetime = datetime.datetime.now()
    created_at: datetime.datetime = datetime.datetime.now()
