from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class StreamCreate(BaseModel):
    streamer_id: str
    game_id: Optional[str] = None
    game_name: Optional[str] = None
    title: str


class StreamResponse(BaseModel):
    id: str
    streamer_id: str
    game_id: Optional[str] = None
    game_name: Optional[str] = None
    title: str
    viewer_count: int
    health_score: float
    is_live: bool
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ViewerUpdate(BaseModel):
    viewer_count: int


class StreamMetricResponse(BaseModel):
    id: str
    stream_id: str
    api_response_time_ms: float
    error_rate: float
    timestamp: Optional[datetime] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    service: str
