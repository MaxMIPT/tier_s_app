import datetime

from sqlalchemy import Column, Enum, String, Integer, DateTime

from db import Base


# TODO: Переименовать WorkflowResult, WorkflowTask -- избавиться от workflow et.c
class WorkflowResult(Base):
    __tablename__ = "workflow_result"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, nullable=False)
    original_file = Column(String, nullable=True)
    converted_file = Column(String, nullable=True)
    restored_text = Column(String, nullable=True)
    voiced_text = Column(String, nullable=True)
    status = Column(Enum("success", "failed", "running", name="workflow_status_enum"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
