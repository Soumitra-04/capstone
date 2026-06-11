# ── Stage 1: dependency cache layer ──────────────────────────────────────────
FROM python:3.11-slim AS deps

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install/pkg -r requirements.txt


# ── Stage 2: lint + test gate ─────────────────────────────────────────────────
FROM python:3.11-slim AS test

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

WORKDIR /app

COPY --from=deps /install/pkg /usr/local

COPY app/ ./app/
COPY tests/ ./tests/

RUN pip install --no-cache-dir flake8 pytest pytest-asyncio \
 && flake8 app/ --max-line-length=120 --ignore=E501,W503 \
 && pytest tests/ -x -q


# ── Stage 3: production runtime ───────────────────────────────────────────────
FROM python:3.11-slim AS runtime

SHELL ["/bin/bash", "-euo", "pipefail", "-c"]

RUN groupadd --system appgroup \
 && useradd  --system --gid appgroup --no-create-home appuser

WORKDIR /app

# ── FIXED: copy from deps stage, not from runtime ──
COPY --from=deps /install/pkg /usr/local
COPY app/ ./app/

RUN chown -R appuser:appgroup /app

USER appuser

ARG WORKERS=2
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen(f'http://localhost:{PORT}/health')"

EXPOSE $PORT

CMD ["sh", "-c", \
  "uvicorn app.main:app \
     --host 0.0.0.0 \
     --port $PORT \
     --workers $WORKERS \
     --no-access-log \
     --proxy-headers"]