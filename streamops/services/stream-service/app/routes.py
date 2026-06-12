import time
import os
import httpx
from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

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
    
    dummy_id = "global-list"
    if not db.query(Stream).filter(Stream.id == dummy_id).first():
        try:
            db.add(Stream(id=dummy_id, streamer_id="system", title="System Target", is_live=False))
            db.commit()
        except Exception:
            db.rollback()
    record_metric(db, dummy_id, elapsed)
    
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


@router.get("/streams/ops/health")
async def ops_health():
    """Ops health status across services."""
    services = [
        {"name": "User Service", "url": "http://user-service:8003/health"},
        {"name": "Stream Service", "url": "http://localhost:8001/health"},
        {"name": "Content Service", "url": "http://content-service:8002/health"},
    ]
    results = []
    async with httpx.AsyncClient(timeout=2.0) as client:
        for s in services:
            start = time.time()
            try:
                resp = await client.get(s["url"])
                resp.raise_for_status()
                latency = int((time.time() - start) * 1000)
                results.append({"name": s["name"], "status": "HEALTHY", "latency_ms": latency})
            except Exception:
                results.append({"name": s["name"], "status": "OFFLINE", "latency_ms": None})
    return {"services": results}


@router.get("/streams/ops/telemetry")
async def ops_telemetry():
    """Ops telemetry and traffic metrics."""
    timeout = httpx.Timeout(2.0)
    latencies = {"user_ms": None, "stream_ms": None, "content_ms": None}
    
    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            start = time.time()
            await client.get("http://user-service:8003/health")
            latencies["user_ms"] = int((time.time() - start) * 1000)
        except Exception: pass
        
        try:
            start = time.time()
            await client.get("http://stream-service:8001/health")
            latencies["stream_ms"] = int((time.time() - start) * 1000)
        except Exception: pass
        
        try:
            start = time.time()
            await client.get("http://content-service:8002/health")
            latencies["content_ms"] = int((time.time() - start) * 1000)
        except Exception: pass

    # get prometheus metrics
    total_requests = 0
    total_errors = 0
    
    for metric in REGISTRY.collect():
        if metric.name == 'http_requests':
            for sample in metric.samples:
                if sample.name == 'http_requests_total':
                    total_requests += sample.value
                    if sample.labels.get('status', '').startswith('5'):
                        total_errors += sample.value
        elif metric.name == 'http_request_exceptions':
            for sample in metric.samples:
                if sample.name == 'http_request_exceptions_total':
                    total_errors += sample.value
                
    error_count = int(total_errors)
    error_rate_pct = round((error_count / total_requests * 100), 2) if total_requests > 0 else 0.0
    success_rate_pct = 100.0 - error_rate_pct
    
    version = os.getenv("APP_VERSION", "v1.0.0")
    environment = os.getenv("ENVIRONMENT", "local")
    git_sha = os.getenv("GIT_SHA", "unknown")
    
    return {
        "latency": latencies,
        "traffic": {
            "total_requests": int(total_requests),
            "error_count": error_count,
            "error_rate_pct": error_rate_pct,
            "success_rate_pct": success_rate_pct
        },
        "deployment": {
            "version": version,
            "environment": environment,
            "git_sha": git_sha
        }
    }


@router.get("/streams/ops/last-load-test")
def ops_last_load_test(db: Session = Depends(get_db)):
    """Query StreamMetric for last 500 records."""
    metrics = db.query(StreamMetric).order_by(StreamMetric.timestamp.desc()).limit(500).all()
    
    total_count = len(metrics)
    if total_count == 0:
        return {
            "avg_response_time_ms": 0,
            "p95_response_time_ms": 0,
            "error_count": 0,
            "total_count": 0
        }
        
    response_times = sorted([m.api_response_time_ms for m in metrics])
    avg_rt = sum(response_times) / total_count
    
    p95_idx = int(total_count * 0.95) - 1
    p95_rt = response_times[max(0, p95_idx)]
    
    error_count = sum(1 for m in metrics if m.error_rate > 0)
    
    return {
        "avg_response_time_ms": int(avg_rt),
        "p95_response_time_ms": int(p95_rt),
        "error_count": error_count,
        "total_count": total_count
    }
