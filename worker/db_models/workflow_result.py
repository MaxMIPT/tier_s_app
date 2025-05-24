from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class WorkflowResult(Base):
    __tablename__ = "workflow_result"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    workflow_id = Column(String, unique=True, nullable=False)
    original_file = Column(String, nullable=True)
    converted_file = Column(String, nullable=True)
    restored_text = Column(String, nullable=True)
    voiced_text = Column(String, nullable=True)
