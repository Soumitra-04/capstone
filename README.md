# 🎮 VibeSync — DevOps Pipeline for Gaming & Live Streaming Platforms

[![CI/CD Pipeline](https://github.com/Soumitra-04/streamops/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/Soumitra-04/streamops/actions)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestrated-326CE5?logo=kubernetes)](https://kubernetes.io/)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus%20%2B%20Grafana-E6522C?logo=prometheus)](https://prometheus.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A production-grade DevOps pipeline simulating the infrastructure behind real-time gaming and live streaming platforms like Twitch and YouTube Live. Built as a capstone project demonstrating CI/CD, containerization, Kubernetes orchestration, and full observability.

---

## 📋 Table of Contents

- [About the Project](#about-the-project)
- [Architecture](#architecture)
- [Microservices](#microservices)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Setup (Docker Compose)](#local-setup-docker-compose)
  - [Kubernetes Setup (Minikube)](#kubernetes-setup-minikube)
- [CI/CD Pipeline](#cicd-pipeline)
- [Monitoring & Observability](#monitoring--observability)
- [API Reference](#api-reference)
- [Load Simulation](#load-simulation)
- [Versioning](#versioning)
- [Roadmap](#roadmap)
- [Authors](#authors)
- [License](#license)

---

## About the Project

StreamOps is a microservices-based backend platform that replicates the DevOps architecture powering real-time gaming and streaming services. The project doesn't stream actual video — instead, it models the **platform layer**: stream sessions, content catalogs, and user management, all instrumented to demonstrate how modern DevOps teams manage high-throughput, low-latency APIs at scale.

**Why this exists:**
- Demonstrate a real-world 3-microservice architecture with independent deployments
- Show automated CI/CD — failing a unit test blocks deployment entirely
- Prove Kubernetes self-healing live: kill a pod, watch it restart
- Visualize API latency, request rates, and error rates in real time via Grafana

**Real-world parallel:** This is structurally identical to how Twitch manages their stream ingestion service, content discovery API, and user identity layer as separate, independently deployable services.

---

## Architecture

```
                        ┌─────────────────────────┐
                        │    React Frontend (Vite) │
                        │       port: 3000         │
                        └────────────┬────────────┘
                                     │ HTTP
                        ┌────────────▼────────────┐
                        │    Nginx API Gateway     │
                        │       port: 80           │
                        └──────┬─────────┬────────┘
                               │         │         │
               ┌───────────────▼─┐  ┌────▼──────┐  ┌▼──────────────┐
               │  Stream Service │  │  Content  │  │  User Service  │
               │   port: 8001    │  │  Service  │  │   port: 8003   │
               │                 │  │ port:8002 │  │                │
               └───────┬─────────┘  └────┬──────┘  └──────┬─────────┘
                       │                 │                 │
               ┌───────▼─────────┐  ┌────▼──────┐  ┌──────▼─────────┐
               │  PostgreSQL DB  │  │ PostgreSQL │  │  PostgreSQL DB  │
               │  (streams_db)   │  │(content_db│  │   (users_db)    │
               └─────────────────┘  └───────────┘  └────────────────┘

                        ┌──────────────────────────┐
                        │   Prometheus + Grafana   │
                        │  Scrapes all 3 services  │
                        │  port: 9090 / 3001       │
                        └──────────────────────────┘
```

**Key design decisions:**
- Each service owns its own database — no shared DB, true microservice isolation
- Nginx acts as the single entry point, routing by path prefix (`/api/streams`, `/api/games`, `/api/users`)
- Services communicate only via HTTP when necessary — minimal inter-service coupling
- Each service exposes a `/metrics` endpoint scraped by Prometheus

---

## Microservices

### 1. 🎥 Stream Service (`/api/streams`)
Manages live stream sessions — the core of the platform. Tracks active streams, viewer counts, and stream health. This service receives the highest API load and is the primary target for load simulation and latency measurement.

| Endpoint | Method | Description |
|---|---|---|
| `/streams` | GET | List all active streams |
| `/streams` | POST | Start a new stream |
| `/streams/{id}` | GET | Get stream details |
| `/streams/{id}/viewers` | PATCH | Update viewer count |
| `/streams/{id}` | DELETE | End a stream |
| `/metrics` | GET | Prometheus metrics |
| `/health` | GET | Health check |

### 2. 📚 Content Catalog Service (`/api/games`)
Manages game categories and content discovery. Allows browsing streams by game, searching titles, and organizing content.

| Endpoint | Method | Description |
|---|---|---|
| `/games` | GET | List all game categories |
| `/games` | POST | Add a game category |
| `/games/{id}` | GET | Get game details |
| `/games/{id}/streams` | GET | Get streams for a game |
| `/search?q=` | GET | Search streams and games |
| `/metrics` | GET | Prometheus metrics |
| `/health` | GET | Health check |

### 3. 👤 User Service (`/api/users`)
Handles identity, authentication, and social graph (follows). Every stream and interaction references a user ID from this service.

| Endpoint | Method | Description |
|---|---|---|
| `/users/register` | POST | Register a new user |
| `/users/login` | POST | Login, returns auth token |
| `/users/{id}` | GET | Get user profile |
| `/users/{id}/follow/{streamer_id}` | POST | Follow a streamer |
| `/users/{id}/following` | GET | Get following list |
| `/metrics` | GET | Prometheus metrics |
| `/health` | GET | Health check |

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Python 3.11 + FastAPI | REST APIs — async, fast, auto-generates OpenAPI docs |
| **Database** | PostgreSQL 15 | One instance per service |
| **Frontend** | React 18 + Vite | Dashboard UI consuming all three APIs |
| **API Gateway** | Nginx | Single entry point, path-based routing |
| **Containerization** | Docker + Docker Compose | Local dev and service isolation |
| **Orchestration** | Kubernetes (Minikube) | Production-like deployment, self-healing |
| **CI/CD** | GitHub Actions | Automated test → build → push pipeline |
| **Registry** | GitHub Container Registry (GHCR) | Docker image storage with versioned tags |
| **Monitoring** | Prometheus + Grafana | Metrics scraping, dashboards, alerting |
| **Load Testing** | Python (httpx + asyncio) | Simulates concurrent API traffic for demos |

---

## Repository Structure

```
streamops/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml               # GitHub Actions pipeline
│
├── services/
│   ├── stream-service/
│   │   ├── app/
│   │   │   ├── main.py             # FastAPI app + Prometheus instrumentation
│   │   │   ├── models.py           # SQLAlchemy models
│   │   │   ├── routes.py           # API route handlers
│   │   │   └── database.py         # DB connection + session
│   │   ├── tests/
│   │   │   └── test_routes.py      # Pytest unit tests
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── content-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── database.py
│   │   ├── tests/
│   │   │   └── test_routes.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── user-service/
│       ├── app/
│       │   ├── main.py
│       │   ├── models.py
│       │   ├── routes.py
│       │   └── database.py
│       ├── tests/
│       │   └── test_routes.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── Dockerfile
│   └── package.json
│
├── nginx/
│   └── nginx.conf                  # Reverse proxy + routing config
│
├── k8s/
│   ├── stream-service.yaml         # Deployment + Service manifest
│   ├── content-service.yaml
│   ├── user-service.yaml
│   ├── frontend.yaml
│   └── ingress.yaml                # Kubernetes Ingress
│
├── monitoring/
│   ├── prometheus.yml              # Scrape config for all 3 services
│   └── grafana-dashboard.json      # Pre-built dashboard export
│
├── scripts/
│   └── load_simulator.py           # Async load generator for demo
│
├── docker-compose.yml              # Full local stack
└── README.md
```

---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started) (v24+) and Docker Compose
- [Python 3.11+](https://www.python.org/downloads/) (for load simulator)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) (for Kubernetes setup)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) (for local Kubernetes cluster)

### Local Setup (Docker Compose)

Clone the repository and bring up the full stack:

```bash
git clone https://github.com/Soumitra-04/streamops.git
cd streamops
```

Start all services:

```bash
docker compose up --build
```

Verify all services are running:

```bash
docker compose ps
```

The following will be available:

| Service | URL |
|---|---|
| Frontend | http://localhost:3000 |
| Stream Service | http://localhost/api/streams |
| Content Service | http://localhost/api/games |
| User Service | http://localhost/api/users |
| Stream Service Docs | http://localhost:8001/docs |
| Content Service Docs | http://localhost:8002/docs |
| User Service Docs | http://localhost:8003/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3001 (admin/admin) |

To stop the stack:

```bash
docker compose down
```

To stop and remove all volumes (fresh start):

```bash
docker compose down -v
```

### Kubernetes Setup (Minikube)

Start a local Kubernetes cluster:

```bash
minikube start --driver=docker
```

Apply all manifests:

```bash
kubectl apply -f k8s/
```

Check that all pods are running:

```bash
kubectl get pods
kubectl get services
```

Access the app via Minikube tunnel:

```bash
minikube tunnel
```

**Demo: Watch self-healing in action**

Kill a pod manually and watch Kubernetes restart it automatically:

```bash
# Get the pod name
kubectl get pods

# Delete it
kubectl delete pod <stream-service-pod-name>

# Watch it come back within seconds
kubectl get pods -w
```

---

## CI/CD Pipeline

The pipeline is defined in `.github/workflows/ci-cd.yml` and triggers on every push to `main`.

```
Push to main
    │
    ▼
┌─────────────────────────────────┐
│  Job 1: TEST                    │
│  - Install deps (all 3 services)│
│  - Run pytest for each service  │
│  - ❌ Any failure = pipeline    │
│     stops. No image is built.   │
└────────────────┬────────────────┘
                 │ (only if all tests pass)
                 ▼
┌─────────────────────────────────┐
│  Job 2: BUILD & PUSH            │
│  - Build Docker image per       │
│    service                      │
│  - Tag: :latest                 │
│  - Tag: :v1.0-{git-sha}  ← versioning
│  - Push to GHCR                 │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  Job 3: DEPLOY                  │
│  - Pull latest images           │
│  - Apply k8s manifests          │
│  - Rolling update (zero         │
│    downtime)                    │
└─────────────────────────────────┘
```

To trigger the pipeline, simply push to main:

```bash
git add .
git commit -m "feat: add viewer count endpoint"
git push origin main
```

Watch the pipeline run at: `https://github.com/Soumitra-04/streamops/actions`

---

## Monitoring & Observability

Every service exposes a `/metrics` endpoint in Prometheus format. Prometheus scrapes all three every 15 seconds.

**Grafana Dashboard includes:**
- Request rate per service (req/sec)
- API latency — p50, p95, p99 (milliseconds)
- Error rate per endpoint (4xx, 5xx)
- Active streams count (live business metric)
- Pod restarts (infrastructure health)

**Alerts configured:**
- Error rate > 5% on any service → fires alert
- API latency p99 > 500ms → fires alert

Access Grafana at `http://localhost:3001` (credentials: `admin` / `admin`) and import `monitoring/grafana-dashboard.json` for the pre-built dashboard.

---

## Load Simulation

The load simulator in `scripts/load_simulator.py` generates concurrent API traffic to all three services, making Grafana dashboards live and meaningful during a demo.

```bash
cd scripts
pip install httpx
python load_simulator.py
```

Configurable parameters inside the script:

```python
CONCURRENT_USERS = 50       # simultaneous virtual users
REQUESTS_PER_USER = 100     # requests each user makes
TARGET_SERVICES = [
    "http://localhost/api/streams",
    "http://localhost/api/games",
    "http://localhost/api/users"
]
```

---

## Versioning

Docker images are versioned using **semantic versioning + git SHA**:

```
ghcr.io/Soumitra-04/stream-service:latest
ghcr.io/Soumitra-04/stream-service:v1.0-a3f2c91
ghcr.io/Soumitra-04/stream-service:v1.1-b7d4e02
```

To roll back to a previous version in Kubernetes:

```bash
kubectl set image deployment/stream-service \
  stream-service=ghcr.io/Soumitra-04/stream-service:v1.0-a3f2c91
```

To check rollout history:

```bash
kubectl rollout history deployment/stream-service
```

---

## Roadmap

**Phase 1 — Foundation (Day 1)**
- [x] Repository setup and branch strategy
- [x] Three microservices (FastAPI + PostgreSQL)
- [x] Docker Compose local stack
- [x] GitHub Actions CI/CD pipeline
- [x] Image versioning via GHCR

**Phase 2 — Orchestration (Day 2)**
- [ ] Minikube cluster setup
- [ ] Kubernetes manifests for all services
- [ ] Kubernetes Ingress configuration
- [ ] Live pod self-healing demo

**Phase 3 — Observability (Day 3)**
- [ ] Prometheus scraping all services
- [ ] Grafana dashboard with latency + error rate panels
- [ ] Alerting rules (error rate > 5%, latency > 500ms)
- [ ] Load simulator for live demo traffic
- [ ] Full end-to-end demo rehearsal

---


## Contributing

This is a capstone project and not open for external contributions. If you'd like to discuss the architecture or raise a question, feel free to open an issue.

For internal team members — branch strategy:

- `main` is protected. Direct pushes are blocked.
- Work on feature branches: `feature/stream-service`, `feature/k8s-manifests`, etc.
- Open a PR to merge into `main`. Pipeline must be green before merging.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---

> *"You can't fix what you can't see."* — the principle behind every monitoring decision in this project.