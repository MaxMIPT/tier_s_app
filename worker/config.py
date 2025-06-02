import os

from pydantic import BaseModel


class Settings(BaseModel):
    RUN_WORKFLOW_TASK_QUEUE_NAME: str
    CONVERT_API: str
    TEXT_API: str
    AUDIO_API: str


settings = Settings(
    CONVERT_API=os.environ.get("CONVERT_API"),
    TEXT_API=os.environ.get("TEXT_API"),
    AUDIO_API=os.environ.get("AUDIO_API"),
    RUN_WORKFLOW_TASK_QUEUE_NAME=os.environ.get(
        "RUN_WORKFLOW_TASK_QUEUE_NAME"
    ),
)
