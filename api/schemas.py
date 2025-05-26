from enum import Enum
from pydantic import BaseModel

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

    model_config = {
        "from_attributes": True
    }

class WorkflowModel(BaseModel):
    workflow_id: str
    client_id: str

    model_config = {
        "from_attributes": True
    }