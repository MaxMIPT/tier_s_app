import datetime

from sqlalchemy import Column, DateTime, Enum, Integer, String, UUID

from db import Base


class Result(Base):
    """
    Сервисные логи
    """

    __tablename__ = "result"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    workflow_id = Column(UUID, unique=True, nullable=False)
    client_id = Column(String, unique=True, nullable=False)
    original_file = Column(String)
    converted_file = Column(String, nullable=True)
    restored_text = Column(String, nullable=True)
    voiced_text = Column(String, nullable=True)
    status = Column(
        Enum("success", "failed", "running", name="ResultStatus"), nullable=False
    )
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
