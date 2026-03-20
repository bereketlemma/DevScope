# DevScope Architecture

## Overview

DevScope is a distributed engineering productivity platform that correlates GitHub metrics with BigQuery analytics to detect anomalies in repository development patterns.

## System Architecture

```
┌─────────────┐
│  GitHub API │
└──────┬──────┘
       │
       ▼
   ┌────────────────────┐
   │  FastAPI Backend   │
   │  + JWT Auth        │
   └────┬───────────┬───┘
        │           │
        ▼           ▼
   ┌─────────┐  ┌──────────────┐
   │   DB    │  │   Celery     │
   │(Postgres)  │   Workers    │
   └─────────┘  └────┬────────┬┘
                     │        │
              ┌──────▼─┐    ┌─▼──────┐
              │ Redis  │    │BigQuery│
              │(Cache) │    │(Events)│
              └────────┘    └──┬─────┘
                               │
                            ┌──▼────┐
                            │ React  │
                            │ Dash   │
                            └────────┘
```

## Components

### Backend (FastAPI)
- REST API for authentication, repo management, and metrics
- GitHub OAuth2 integration
- JWT token-based authorization
- Async database queries with SQLAlchemy 2.0
- Connection pooling and caching

### Database Layer
- **PostgreSQL 16**: Application state (users, repos, sync jobs, anomalies)
- **BigQuery**: Analytics data (PR events, commits, metrics)
- **Redis 7**: Caching and Celery task queue

### Task Queue (Celery)
- Background GitHub data sync jobs
- Metric computation tasks
- Anomaly detection
- Jobs tracked in sync_jobs table

### Frontend (React 18)
- TypeScript strict mode
- Vite dev server
- Tailwind CSS styling
- Recharts for metrics visualization
- Zustand for state management

## Data Flow

### Milestone 1: Core Platform

1. **User Authentication**
   - GitHub OAuth → JWT token
   - Store user in PostgreSQL

2. **Repository Sync (Celery Task)**
   - Fetch PR/commit/review data from GitHub API
   - Write app state to PostgreSQL
   - Write events to BigQuery

3. **Metrics Computation**
   - Query BigQuery for events (last 30 days)
   - Calculate PR latency, review cycles, commit frequency
   - Detect anomalies via Z-score ($ |z| > 3 $)
   - Store anomalies in PostgreSQL

4. **Dashboard**
   - Fetch repos from PostgreSQL
   - Query metrics from BigQuery
   - Display charts and anomaly feed

### Milestone 2: Cloud-Native Upgrade
- GitHub Webhooks → Pub/Sub → Dataflow → BigQuery
- Vertex AI anomaly detection
- Event-driven architecture

## Database Schema

### PostgreSQL (app_data)

**users**
- id, github_id (unique), username, email, avatar_url, access_token
- created_at, updated_at

**repositories**
- id, github_id (unique), owner, name, full_name, url
- stars, watchers, forks, language, is_fork
- created_at, updated_at, last_synced_at

**sync_jobs**
- id, repository_id, status (pending|running|success|failed)
- error_message, started_at, completed_at, created_at

**anomalies**
- id, repository_id, metric_name, detected_value, z_score, threshold
- description, created_at

### BigQuery (analytics)

**pull_requests**
- event_id, repository_id, pr_number
- author, title, state
- created_at, closed_at, review_comments
- additions, deletions

**commits**
- event_id, repository_id, sha, author
- message, created_at
- files_changed, insertions, deletions

**reviews**
- event_id, pr_number, reviewer, state
- submitted_at

## Security

- **Auth**: GitHub OAuth2 + JWT (HS256)
- **API**: CORS middleware, request validation with Pydantic
- **DB**: Async drivers, parameterized queries (SQLAlchemy ORM)
- **Secrets**: Environment variables for API keys, GCP credentials
- **Monitoring**: Correlation IDs for request tracing

## Deployment

### Docker Compose (Local)
- Postgres 16, Redis 7, FastAPI backend, Celery worker, React frontend
- Environment variables from `.env`

### Google Cloud (Production)
- **Cloud Run**: Backend + Frontend
- **Cloud SQL**: PostgreSQL instance
- **Memorystore**: Redis
- **BigQuery**: Analytics warehouse
- **Cloud Scheduler**: Periodic sync jobs

## Performance Optimizations

- BigQuery caching (Redis)
- Connection pooling (PostgreSQL)
- Async I/O (FastAPI + SQLAlchemy)
- GitHub API pagination (100 items/page)
- Frontend code splitting (Vite)
- Lazy loading (React Router)

## Monitoring & Observability

- Structured logging with correlation IDs
- Sentry for error tracking
- Celery task monitoring
- Database query logging (debug mode)
- Frontend performance metrics

## CI/CD Pipeline

- **CI**: GitHub Actions (tests, linting, type checking)
- **CodeQL**: Security analysis
- **Dependabot**: Dependency updates
- **CD**: Manual or automated deployment to Cloud Run

## Development Workflow

1. `make install` — Install dependencies
2. `make dev` — Start Docker Compose with all services
3. `make format` — Format code
4. `make lint` — Run linters
5. `make test` — Run tests
6. Create PR with conventional commit message
7. CI runs automatically
8. Deploy on merge to main
