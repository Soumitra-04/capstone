import os
import time
import random
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import httpx
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

from app.database import get_db
from app.models import Game, Recommendation
from app.schemas import GameCreate, GameResponse, RecommendationResponse, HealthResponse

router = APIRouter()

STREAM_SERVICE_URL = os.getenv("STREAM_SERVICE_URL", "http://localhost:8001")

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"])


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "content-service"}


@router.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.post("/games", response_model=GameResponse, status_code=201)
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    """Create a new game category."""
    start = time.time()
    existing = db.query(Game).filter(Game.name == game.name).first()
    if existing:
        REQUEST_COUNT.labels("POST", "/games", "400").inc()
        logger.warning(f"Failed to create game: Game '{game.name}' already exists")
        raise HTTPException(status_code=400, detail="Game already exists")

    db_game = Game(name=game.name, description=game.description)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    elapsed = (time.time() - start) * 1000
    REQUEST_COUNT.labels("POST", "/games", "201").inc()
    REQUEST_DURATION.labels("POST", "/games").observe(elapsed / 1000)
    logger.info(f"Successfully created game '{db_game.name}' with id {db_game.id}")
    return db_game


@router.get("/games", response_model=List[GameResponse])
def list_games(db: Session = Depends(get_db)):
    """List all games."""
    start = time.time()
    games = db.query(Game).all()
    elapsed = (time.time() - start) * 1000
    REQUEST_COUNT.labels("GET", "/games", "200").inc()
    REQUEST_DURATION.labels("GET", "/games").observe(elapsed / 1000)
    return games


@router.get("/games/{game_id}", response_model=GameResponse)
def get_game(game_id: str, db: Session = Depends(get_db)):
    """Get game details by ID."""
    start = time.time()
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        REQUEST_COUNT.labels("GET", "/games/{id}", "404").inc()
        raise HTTPException(status_code=404, detail="Game not found")
    elapsed = (time.time() - start) * 1000
    REQUEST_COUNT.labels("GET", "/games/{id}", "200").inc()
    REQUEST_DURATION.labels("GET", "/games/{id}").observe(elapsed / 1000)
    return game


@router.get("/games/{game_id}/streams")
def get_game_streams(game_id: str, db: Session = Depends(get_db)):
    """Get streams for a game by calling stream-service."""
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")

    try:
        with httpx.Client(timeout=5.0) as client:
            response = client.get(f"{STREAM_SERVICE_URL}/streams")
            if response.status_code == 200:
                all_streams = response.json()
                game_streams = [s for s in all_streams if s.get("game_id") == game_id]
                return {"game": game.name, "streams": game_streams}
            return {"game": game.name, "streams": [], "error": "Stream service returned non-200"}
    except httpx.RequestError as e:
        logger.error(f"Error calling stream-service for game {game_id}: {e}", exc_info=True)
        return {"game": game.name, "streams": [], "error": "Stream service unavailable"}


@router.get("/recommendations/{user_id}", response_model=List[RecommendationResponse])
def get_recommendations(user_id: str, db: Session = Depends(get_db)):
    """Get recommendations for a user. Simple: recommend popular games."""
    existing = db.query(Recommendation).filter(Recommendation.user_id == user_id).all()
    if existing:
        return existing

    games = db.query(Game).all()
    if not games:
        return []

    recommendations = []
    for game in games[:5]:
        rec = Recommendation(
            user_id=user_id,
            recommended_game_id=game.id,
            game_name=game.name,
            score=round(random.uniform(0.5, 1.0), 2),
        )
        db.add(rec)
        recommendations.append(rec)
    db.commit()
    for rec in recommendations:
        db.refresh(rec)
    return recommendations


@router.get("/search", response_model=List[GameResponse])
def search_games(q: Optional[str] = Query(None, min_length=1), db: Session = Depends(get_db)):
    """Search games by name."""
    if not q:
        raise HTTPException(status_code=400, detail="Query parameter 'q' is required")
    games = db.query(Game).filter(Game.name.ilike(f"%{q}%")).all()
    return games
