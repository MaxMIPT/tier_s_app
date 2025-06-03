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
    converted_file: str | None = Field(None)
    restored_text: str | None = Field(None)
    voiced_text: str | None = Field(None)
    status: ResultStatus


class UpdateResultModel(BaseSchema):
    workflow_id: UUID
    status: ResultStatus
    converted_file: Optional[str] = (None,)
    restored_text: Optional[str] = (None,)
    voiced_text: Optional[str] = None


class TaskModel(BaseSchema):
    client_id: str
    workflow_id: UUID
    status: TaskStatus
    created_at: datetime.datetime = datetime.datetime.now()


class Task_x_Result(BaseSchema):
    id: int
    client_id: str
    workflow_id: UUID
    status: TaskStatus
    created_at: datetime.datetime = datetime.datetime.now()
    original_file_url: Optional[str] = (None,)
    pipeline_status: ResultStatus
    process_converted_file_url: Optional[str] = (None,)
    process_transcripted_text: Optional[str] = (None,)
    process_dubbed_file_url: Optional[str] = (None,)

