from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class WorkflowTask(Base):
    __tablename__ = "workflow_tasks"

    client_id = Column(String, unique=True, primary_key=True)
    workflow_id = Column(String, unique=True, primary_key=True)