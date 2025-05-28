import datetime

from sqlalchemy import Column, String, DateTime

from db import Base


class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"

    client_id = Column(String, primary_key=True)
    workflow_id = Column(String, primary_key=True)
    event_type = Column(String,)  # enum
    status = Column(String,)  # success, error
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
