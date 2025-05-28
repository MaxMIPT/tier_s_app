import datetime

from sqlalchemy import Column, String, DateTime

from db import Base

<<<<<<< Updated upstream:api/db_models/workflow.py

class WorkflowTask(Base):
=======
class Task(Base):
>>>>>>> Stashed changes:api/db_models/Task.py
    __tablename__ = "workflow_tasks"

    client_id = Column(String, primary_key=True)
    workflow_id = Column(String, primary_key=True)
    event_type = Column(String,)  # enum
    status = Column(String,)  # success, error
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
