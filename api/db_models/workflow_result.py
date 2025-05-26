from sqlalchemy import Column, Enum, String, Integer
from db import Base

class WorkflowResult(Base):
    __tablename__ = "workflow_result"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, nullable=False)
    original_file = Column(String, nullable=True)
    converted_file = Column(String, nullable=True)
    restored_text = Column(String, nullable=True)
    voiced_text = Column(String, nullable=True)
    status = Column(Enum("success", "failed", "running", name="workflow_status_enum"), nullable=True)