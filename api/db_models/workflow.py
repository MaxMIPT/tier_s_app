from sqlalchemy import Column, String
from db import Base

class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"

    client_id = Column(String, primary_key=True)
    workflow_id = Column(String, primary_key=True)