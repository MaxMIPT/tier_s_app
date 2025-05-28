from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ResultStatus(str, Enum):
    success = "success"
    failed = "failed"
    running = "running"

class TaskStatus(str, Enum):
    CREATED = 'created'
    AUDIO_CONVERSION_STARTED = 'audio_conversion_started'
    AUDIO_CONVERSION_FINISHED = 'audio_conversion_finished'
    AUDIO_TRANSCRIPTION_STARTED = 'audio_transcription_started'
    AUDIO_TRANSCRIPTION_FINISHED = 'audio_transcription_finished'
    AUDIO_DUBBING_STARTED = 'audio_dubbing_started'
    AUDIO_DUBBING_FINISHED = 'audio_dubbing_finished'
    FINISHED = 'finished'
    CANCELED = 'canceled'

class ResultModel(BaseModel):
    workflow_id: str 
    client_id: str
    original_file: str | None
    converted_file: str | None
    restored_text: str | None
    voiced_text: str | None
    status: ResultStatus

    model_config = {
        "from_attributes": True
    }

class UpdateResultModel(BaseModel):
    workflow_id: str
    status: ResultStatus
    converted_file: Optional[str] = None, 
    restored_text: Optional[str] = None, 
    voiced_text: Optional[str] = None

class TaskModel(BaseModel):

    client_id: str
    workflow_id: str
    status: TaskStatus

    model_config = {
        "from_attributes": True
    }