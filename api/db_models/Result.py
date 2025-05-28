import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String

from db import Base

# сервисные логи

class Result(Base):
    __tablename__ = "result"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    workflow_id = Column(String, unique=True, nullable=False)
    client_id = Column(String, unique=True, nullable=False)
    original_file = Column(String)
    converted_file = Column(String, nullable=True)
    restored_text = Column(String, nullable=True)
    voiced_text = Column(String, nullable=True)
    status = Column(Enum("success",
                        "failed",
                        "running", 
                        name="RusultStatus"), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
