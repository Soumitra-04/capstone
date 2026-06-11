import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Stream(Base):
    __tablename__ = "streams"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    streamer_id = Column(String, nullable=False)
    game_id = Column(String, nullable=True)
    game_name = Column(String, nullable=True)
    title = Column(String, nullable=False)
    viewer_count = Column(Integer, default=0)
    health_score = Column(Float, default=100.0)
    is_live = Column(Boolean, default=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ended_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    metrics = relationship("StreamMetric", back_populates="stream", cascade="all, delete-orphan")


class StreamMetric(Base):
    __tablename__ = "stream_metrics"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    stream_id = Column(String, ForeignKey("streams.id"), nullable=False)
    api_response_time_ms = Column(Float, nullable=False)
    error_rate = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    stream = relationship("Stream", back_populates="metrics")
