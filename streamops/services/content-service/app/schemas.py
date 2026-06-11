from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class GameCreate(BaseModel):
    name: str
    description: Optional[str] = None


class GameResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class RecommendationResponse(BaseModel):
    id: str
    user_id: str
    recommended_stream_id: Optional[str] = None
    recommended_game_id: str
    game_name: Optional[str] = None
    score: float
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str
    service: str
