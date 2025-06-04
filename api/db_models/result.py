import datetime

from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, UUID

from .base import Base


class Result(Base):
    """
    Сервисные логи
    """

    __tablename__ = "result"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    workflow_id = Column(UUID, unique=True, nullable=False)
    client_id = Column(String, nullable=False)
    original_file_name = Column(String)
    original_file = Column(String)
    converted_file = Column(String, nullable=True)
    converted_file_duration = Column(Float, nullable=True)
    restored_text = Column(String, nullable=True)
    dubbed_file = Column(String, nullable=True)
    status = Column(
        Enum("success", "failed", "running", name="ResultStatus"),
        nullable=False,
    )
    created_at = Column(
        DateTime, nullable=False, default=datetime.datetime.now()
    )
