import datetime

from sqlalchemy import Column, DateTime, Integer, String, Enum, UUID

from db import Base


class Task(Base):
    """
    Статусы для вебсокета
    """

    __tablename__ = "task"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, nullable=False)
    workflow_id = Column(UUID, nullable=False)
    status = Column(
        Enum(
            "created",
            "audio_conversion_started",
            "audio_conversion_finished",
            "audio_transcription_started",
            "audio_transcription_finished",
            "audio_dubbing_started",
            "audio_dubbing_finished",
            "finished",
            "canceled",
            name="TaskStatus",
        ),
        nullable=True,
    )
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now())
