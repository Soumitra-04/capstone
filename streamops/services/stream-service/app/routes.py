import time
from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

from app.database import get_db
from app.models import Stream, StreamMetric
from app.schemas import StreamCreate, StreamResponse, ViewerUpdate, HealthResponse

router = APIRouter()

REQUEST_COUNT = Counter("http_requests_total", "Total HTTP requests", ["method", "endpoint", "status"])
REQUEST_DURATION = Histogram("http_request_duration_seconds", "HTTP request duration", ["method", "endpoint"])
ACTIVE_STREAMS = Gauge("streams_active", "Number of active streams")
TOTAL_VIEWERS = Gauge("stream_viewers_total", "Total viewers across all streams")


def record_metric(db: Session, stream_id: str, response_time_ms: float, error: bool = False):
    metric = StreamMetric(
        stream_id=stream_id,
        api_response_time_ms=response_time_ms,
        error_rate=1.0 if error else 0.0,
    )
    db.add(metric)
    db.commit()


def update_gauges(db: Session):
    active = db.query(Stream).filter(Stream.is_live == True).count()
    ACTIVE_STREAMS.set(active)
    total_viewers = sum(
        s.viewer_count for s in db.query(Stream).filter(Stream.is_live == True).all()
    )
    TOTAL_VIEWERS.set(total_viewers)


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "stream-service"}


@router.get("/metrics")
def metrics():
    """Prometheus metrics endpoint."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@router.post("/streams", response_model=StreamResponse, status_code=201)
def create_stream(stream: StreamCreate, db: Session = Depends(get_db)):
    """Start a new stream."""
    start = time.time()
    try:
        db_stream = Stream(
            streamer_id=stream.streamer_id,
            game_id=stream.game_id,
            game_name=stream.game_name,
            title=stream.title,
        )
        db.add(db_stream)
        db.commit()
        db.refresh(db_stream)
        update_gauges(db)
        elapsed = (time.time() - start) * 1000
        record_metric(db, db_stream.id, elapsed)
        REQUEST_COUNT.labels("POST", "/streams", "201").inc()
        REQUEST_DURATION.labels("POST", "/streams").observe(elapsed / 1000)
        return db_stream
    except Exception as e:
        elapsed = (time.time() - start) * 1000
        REQUEST_COUNT.labels("POST", "/streams", "500").inc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/streams", response_model=List[StreamResponse])
def list_streams(db: Session = Depends(get_db)):
    """List all live streams."""
    start = time.time()
    streams = db.query(Stream).filter(Stream.is_live == True).all()
    elapsed = (time.time() - start) * 1000
    REQUEST_COUNT.labels("GET", "/streams", "200").inc()
    REQUEST_DURATION.labels("GET", "/streams").observe(elapsed / 1000)
    return streams


@router.get("/streams/{stream_id}", response_model=StreamResponse)
def get_stream(stream_id: str, db: Session = Depends(get_db)):
    """Get stream details by ID."""
    start = time.time()
    stream = db.query(Stream).filter(Stream.id == stream_id).first()
    if not stream:
        REQUEST_COUNT.labels("GET", "/streams/{id}", "404").inc()
        raise HTTPException(status_code=404, detail="Stream not found")
    elapsed = (time.time() - start) * 1000
    record_metric(db, stream.id, elapsed)
    REQUEST_COUNT.labels("GET", "/streams/{id}", "200").inc()
    REQUEST_DURATION.labels("GET", "/streams/{id}").observe(elapsed / 1000)
    return stream


@router.patch("/streams/{stream_id}/viewers", response_model=StreamResponse)
def update_viewers(stream_id: str, update: ViewerUpdate, db: Session = Depends(get_db)):
    """Update viewer count for a stream."""
    start = time.time()
    stream = db.query(Stream).filter(Stream.id == stream_id).first()
    if not stream:
        REQUEST_COUNT.labels("PATCH", "/streams/{id}/viewers", "404").inc()
        raise HTTPException(status_code=404, detail="Stream not found")
    stream.viewer_count = update.viewer_count
    db.commit()
    db.refresh(stream)
    update_gauges(db)
    elapsed = (time.time() - start) * 1000
    record_metric(db, stream.id, elapsed)
    REQUEST_COUNT.labels("PATCH", "/streams/{id}/viewers", "200").inc()
    REQUEST_DURATION.labels("PATCH", "/streams/{id}/viewers").observe(elapsed / 1000)
    return stream


@router.delete("/streams/{stream_id}", response_model=StreamResponse)
def end_stream(stream_id: str, db: Session = Depends(get_db)):
    """End a stream."""
    start = time.time()
    stream = db.query(Stream).filter(Stream.id == stream_id).first()
    if not stream:
        REQUEST_COUNT.labels("DELETE", "/streams/{id}", "404").inc()
        raise HTTPException(status_code=404, detail="Stream not found")
    stream.is_live = False
    stream.ended_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(stream)
    update_gauges(db)
    elapsed = (time.time() - start) * 1000
    record_metric(db, stream.id, elapsed)
    REQUEST_COUNT.labels("DELETE", "/streams/{id}", "200").inc()
    REQUEST_DURATION.labels("DELETE", "/streams/{id}").observe(elapsed / 1000)
    return stream
