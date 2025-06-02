from enum import Enum
from pydantic import BaseModel, Field


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
    workflow_id: str | None
    client_id: str
    original_file: str | None = Field(None)
    converted_file: str | None = Field(None)
    restored_text: str | None = Field(None)
    voiced_text: str | None = Field(None)
    status: ResultStatus


class TaskModel(BaseSchema):

    client_id: str
    workflow_id: str
    status: TaskStatus
