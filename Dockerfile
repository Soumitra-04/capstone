<<<<<<< HEAD
# =============================================================================
# VibeSync API — Multi-Stage Production Dockerfile
# =============================================================================
# Stage 1 (builder): Installs all dependencies including build tools.
# Stage 2 (runtime): Copies only the compiled wheels + app code.
#
# Result: Minimal attack surface, ~150MB final image vs ~800MB naive build.
# =============================================================================

# ---------------------------------------------------------------------------
# STAGE 1: Builder — Install & compile dependencies
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies (gcc, etc.) needed for compiled wheels
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first for Docker layer caching — dependencies change
# less frequently than application code, so this layer is cached across builds
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------------------------------------------------------------------------
# STAGE 2: Runtime — Minimal production image
# ---------------------------------------------------------------------------
FROM python:3.11-slim AS runtime

# Security: Run as non-root user to follow the principle of least privilege
RUN groupadd -r vibesync && useradd -r -g vibesync -d /app -s /sbin/nologin vibesync

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy application source code
COPY streamops/services/ ./services/

# Expose the default FastAPI/Uvicorn port
EXPOSE 8000

# Health check for container orchestrators (Docker Compose, Kubernetes)
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Switch to non-root user
USER vibesync

# Production-grade Uvicorn configuration:
#   --host 0.0.0.0    : Bind to all interfaces (required in containers)
#   --workers 4       : Multi-process for CPU utilization (adjust per pod CPU limit)
#   --no-access-log   : Reduce I/O overhead; use structured logging instead
CMD ["uvicorn", "services.stream-service.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--no-access-log"]
=======
# Stage 1 - Builder
FROM python:3.11 AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Stage 2 - Runtime
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
>>>>>>> 182ad04 (Initial commit)
