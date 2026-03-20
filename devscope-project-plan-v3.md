# DevScope — Repository Intelligence Tool
## Complete Project Plan & Build Guide (v3 — Final)

---

## 1. PROJECT OVERVIEW

**What DevScope Does:**
A distributed engineering productivity platform that mines GitHub repositories via the GitHub API, correlates developer metrics (PR latency, code churn, review cycles), streams events through Google Cloud Pub/Sub into BigQuery for sub-second querying, and uses Vertex AI for time-series anomaly detection — all surfaced through a React/TypeScript dashboard.

**Full Tech Stack:**

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, TypeScript (strict), Vite, TailwindCSS, Recharts |
| Backend API | Python 3.11+, FastAPI, Pydantic v2 |
| App Database | PostgreSQL 16, SQLAlchemy 2.0 (async), Alembic |
| Analytics Warehouse | Google BigQuery |
| Caching | Redis 7 |
| Task Queue | Celery + Redis broker |
| Authentication | GitHub OAuth2 + JWT (PyJWT) |
| Streaming (M2) | Google Cloud Pub/Sub |
| Stream Processing (M2) | Apache Beam → Cloud Dataflow |
| ML (M2) | Vertex AI (AutoML or IsolationForest) |
| Deployment | Docker, Cloud Run, Cloud SQL, Memorystore (Redis) |
| CI/CD | GitHub Actions |
| Monitoring | Sentry, structured logging with correlation IDs |
| Code Quality | Ruff, ESLint, Prettier, pre-commit, Dependabot |

---

## 2. MILESTONE STRATEGY

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  MILESTONE 1 — "DevScope Core" (Weeks 1–4)                                   │
│  Demo-ready. Resume-valid. Production-grade architecture.                    │
│                                                                              │
│  GitHub OAuth ──► FastAPI + JWT ──► PostgreSQL (app data)                    │
│        │                               │                                     │
│        └──► Celery Workers ──► BigQuery (analytics)                          │
│                                   │                                          │
│                            Metrics SQL ──► React Dashboard                   │
│                                   │                                          │
│                            Z-Score Anomalies ──► Alert Feed                  │
│                                                                              │
│  + Redis caching, connection pooling, API pagination, error tracking,        │
│    CI/CD, Docker, Cloud Run, accessibility, correlation IDs                  │
│                                                                              │
│  Week 1: Foundation (scaffolding, GCP, Postgres, BigQuery, GitHub client)    │
│  Week 2: Backend (FastAPI, auth, Redis, Celery, ingestion pipeline)          │
│  Week 3: Metrics + Dashboard (computation, charts, anomalies, repo detail)   │
│  Week 4: Deploy + Polish (Docker, Cloud Run, CI/CD, docs, accessibility)     │
├──────────────────────────────────────────────────────────────────────────────┤
│  MILESTONE 2 — "DevScope Advanced" (Weeks 5–6)                               │
│  Cloud-native upgrade on top of a working system.                            │
│                                                                              │
│  GitHub Webhooks ──► Pub/Sub ──► Dataflow ──► BigQuery                       │
│                                   Vertex AI anomaly detection                │
│                                                                              │
│  Week 5: Real-Time Pipeline (Pub/Sub + Webhooks + Dataflow)                  │
│  Week 6: ML Anomaly Detection (Vertex AI) + Final Polish                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

**Data Flow Architecture (Milestone 1):**
```
GitHub API
    │
    ▼
┌─────────────────────────────────────────────┐
│ Celery Worker (background job)              │
│                                             │
│  1. Fetch PRs, commits, reviews from GitHub │
│  2. Write app state to PostgreSQL           │
│     (repos, sync jobs, anomaly records)     │
│  3. Write analytical data to BigQuery       │
│     (raw events, PRs, commits, reviews)     │
│  4. Update sync status in PostgreSQL        │
└─────────────────────────────────────────────┘
    │                    │
    ▼                    ▼
PostgreSQL           BigQuery
(app data)           (analytics)
    │                    │
    ▼                    ▼
FastAPI reads        FastAPI runs
repos, users,        metric aggregation
jobs, anomalies      SQL queries
    │                    │
    └────────┬───────────┘
             ▼
        React Dashboard
```

**PostgreSQL owns:** users, sessions, repositories (CRUD), sync jobs, anomaly records, API keys, settings
**BigQuery owns:** raw GitHub events, pull request analytics, commit analytics, review analytics, daily aggregated metrics

---

## 3. INDUSTRY-STANDARD PROJECT STRUCTURE

```
devscope/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                    # Lint + test on every PR
│   │   ├── cd.yml                    # Deploy to Cloud Run on merge to main
│   │   └── codeql.yml                # Security scanning
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── feature_request.md
│   │   └── task.md
│   └── dependabot.yml                # Automated dependency updates
│
├── docs/
│   ├── architecture.md               # System architecture diagram + decisions
│   ├── api-reference.md              # API endpoint documentation
│   ├── data-model.md                 # Postgres + BigQuery schemas
│   ├── setup-guide.md                # Local dev + GCP setup instructions
│   ├── deployment.md                 # Cloud Run deployment runbook
│   └── adr/                          # Architecture Decision Records
│       ├── 001-postgres-plus-bigquery.md
│       ├── 002-celery-for-background-jobs.md
│       ├── 003-jwt-auth-with-github-oauth.md
│       ├── 004-pubsub-over-kafka.md          # (M2)
│       └── 005-vertex-ai-anomaly-detection.md # (M2)
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point + lifespan
│   │   ├── config.py                 # Environment config (pydantic-settings)
│   │   ├── dependencies.py           # Dependency injection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py             # Top-level router aggregation
│   │   │   ├── middleware/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # JWT verification middleware
│   │   │   │   ├── correlation_id.py # Request ID injection
│   │   │   │   ├── rate_limit.py     # slowapi rate limiting
│   │   │   │   └── error_handler.py  # Global exception → error envelope
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py           # /api/v1/auth — GitHub OAuth + JWT
│   │   │   │   ├── repos.py          # /api/v1/repos — repo CRUD
│   │   │   │   ├── metrics.py        # /api/v1/metrics — query metrics
│   │   │   │   ├── anomalies.py      # /api/v1/anomalies — anomaly results
│   │   │   │   ├── health.py         # /api/v1/health — liveness + readiness
│   │   │   │   └── webhooks.py       # /api/v1/webhooks — GitHub webhooks (M2)
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── github_client.py      # GitHub API wrapper (REST + GraphQL)
│   │   │   ├── pubsub_publisher.py   # Pub/Sub message publishing (M2)
│   │   │   ├── bigquery_client.py    # BigQuery read/write operations
│   │   │   ├── redis_client.py       # Redis connection + cache helpers
│   │   │   └── vertex_client.py      # Vertex AI inference client (M2)
│   │   │
│   │   ├── db/
│   │   │   ├── __init__.py
│   │   │   ├── engine.py             # SQLAlchemy async engine + session factory
│   │   │   ├── models.py             # ORM models (User, Repo, SyncJob, Anomaly)
│   │   │   └── repositories/         # Repository pattern for DB access
│   │   │       ├── __init__.py
│   │   │       ├── user_repo.py
│   │   │       ├── repo_repo.py
│   │   │       ├── sync_job_repo.py
│   │   │       └── anomaly_repo.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py       # OAuth flow + JWT generation
│   │   │   ├── repo_service.py       # Business logic: repo onboarding
│   │   │   ├── metrics_service.py    # Business logic: metric computation
│   │   │   ├── ingestion_service.py  # Business logic: event ingestion
│   │   │   └── anomaly_service.py    # Business logic: anomaly detection
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py            # Pydantic request/response schemas
│   │   │   ├── enums.py              # Shared enums
│   │   │   └── envelope.py           # API response envelope wrapper
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── rate_limiter.py       # GitHub API rate limit handling
│   │       ├── circuit_breaker.py    # Circuit breaker for external services
│   │       ├── sanitizer.py          # Input sanitization
│   │       └── logger.py             # Structured logging + correlation IDs
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── celery_app.py             # Celery configuration
│   │   ├── tasks/
│   │   │   ├── __init__.py
│   │   │   ├── ingestion_tasks.py    # Repo backfill + sync tasks
│   │   │   ├── metrics_tasks.py      # Daily metric aggregation
│   │   │   └── anomaly_tasks.py      # Anomaly detection runs
│   │   ├── event_processor.py        # Pub/Sub subscriber (M2)
│   │   └── batch_ingester.py         # Historical data backfill worker
│   │
│   ├── migrations/
│   │   ├── env.py                    # Alembic environment
│   │   ├── alembic.ini               # Alembic config
│   │   └── versions/                 # Migration files
│   │       └── 001_initial_schema.py
│   │
│   ├── dataflow/
│   │   ├── pipeline.py               # Apache Beam pipeline definition (M2)
│   │   └── transforms.py             # Custom PTransforms (M2)
│   │
│   ├── ml/
│   │   ├── train.py                  # Vertex AI training job script (M2)
│   │   ├── predict.py                # Batch/online prediction (M2)
│   │   └── preprocessing.py          # Feature engineering (M2)
│   │
│   ├── tests/
│   │   ├── conftest.py               # Shared fixtures + test DB setup
│   │   ├── factories.py              # Test data factories (factory_boy)
│   │   ├── unit/
│   │   │   ├── test_github_client.py
│   │   │   ├── test_metrics_service.py
│   │   │   ├── test_anomaly_service.py
│   │   │   ├── test_auth_service.py
│   │   │   └── test_sanitizer.py
│   │   ├── integration/
│   │   │   ├── test_api_repos.py
│   │   │   ├── test_api_metrics.py
│   │   │   ├── test_api_auth.py
│   │   │   ├── test_bigquery.py
│   │   │   └── test_celery_tasks.py
│   │   └── e2e/
│   │       └── test_full_pipeline.py
│   │
│   ├── scripts/
│   │   ├── seed_data.py              # Seed both Postgres + BigQuery
│   │   ├── setup_gcp.sh              # One-click GCP resource provisioning
│   │   └── run_backfill.py           # Historical data ingestion
│   │
│   ├── Dockerfile
│   ├── Dockerfile.worker             # Separate image for Celery workers
│   ├── requirements.in               # Unpinned dependencies
│   ├── requirements.txt              # Locked/pinned (generated by pip-compile)
│   ├── requirements-dev.in
│   ├── requirements-dev.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                  # App entry
│   │   ├── App.tsx                   # Root component + routing with lazy loading
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── api/
│   │   │   ├── client.ts             # Axios wrapper — interceptors, error envelope parsing
│   │   │   ├── repos.ts              # Repo API calls
│   │   │   ├── metrics.ts            # Metrics API calls
│   │   │   ├── anomalies.ts          # Anomaly API calls
│   │   │   └── auth.ts               # Auth API calls (login, refresh, logout)
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   ├── DashboardLayout.tsx
│   │   │   │   └── ProtectedRoute.tsx  # Redirect to login if no JWT
│   │   │   ├── charts/
│   │   │   │   ├── PRLatencyChart.tsx
│   │   │   │   ├── CodeChurnChart.tsx
│   │   │   │   ├── ReviewCycleChart.tsx
│   │   │   │   ├── AnomalyTimeline.tsx
│   │   │   │   └── HealthScoreGauge.tsx
│   │   │   ├── repos/
│   │   │   │   ├── RepoCard.tsx
│   │   │   │   ├── RepoList.tsx
│   │   │   │   └── AddRepoModal.tsx
│   │   │   └── common/
│   │   │       ├── LoadingSpinner.tsx
│   │   │       ├── ErrorBoundary.tsx
│   │   │       ├── MetricCard.tsx
│   │   │       ├── DateRangePicker.tsx
│   │   │       └── Pagination.tsx      # Reusable pagination component
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx          # Main overview page
│   │   │   ├── RepoDetail.tsx         # Single repo deep-dive
│   │   │   ├── Anomalies.tsx          # Anomaly feed
│   │   │   ├── Settings.tsx           # User/org settings
│   │   │   ├── Login.tsx              # GitHub OAuth login page
│   │   │   └── Onboarding.tsx         # Add repos after login
│   │   │
│   │   ├── hooks/
│   │   │   ├── useMetrics.ts          # React Query hook for metrics
│   │   │   ├── useRepos.ts            # React Query hook for repos
│   │   │   ├── useAnomalies.ts        # React Query hook for anomalies
│   │   │   └── useAuth.ts             # Auth state + token management
│   │   │
│   │   ├── store/
│   │   │   └── auth.ts               # Auth context (JWT, user info)
│   │   │
│   │   ├── types/
│   │   │   ├── api.ts                # API envelope types
│   │   │   ├── metrics.ts
│   │   │   ├── repos.ts
│   │   │   └── anomalies.ts
│   │   │
│   │   └── utils/
│   │       ├── formatters.ts          # Number/date formatting
│   │       └── constants.ts           # App-wide constants
│   │
│   ├── public/
│   │   └── favicon.svg
│   ├── index.html                     # Includes CSP meta tag
│   ├── vite.config.ts
│   ├── tsconfig.json                  # strict: true
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   ├── package-lock.json              # COMMITTED — locked dependencies
│   ├── .eslintrc.cjs
│   └── .prettierrc
│
├── infra/
│   └── docker-compose.yml            # Postgres + Redis + Backend + Worker + Frontend
│
├── .editorconfig                      # Consistent formatting across editors
├── .pre-commit-config.yaml            # Pre-commit hooks (ruff, eslint, prettier)
├── .gitignore
├── .env.example                       # Template for env vars
├── .env.dev                           # Dev environment defaults (committed, no secrets)
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── Makefile
├── DEV_LOG.md
└── CHANGELOG.md
```

---

## 4. COMPLETE FEATURE LIST

### 4.1 — Authentication & Authorization

- [ ] GitHub OAuth2 login flow (register OAuth app, handle callback)
- [ ] JWT access tokens (15-min expiry) + refresh tokens (7-day, stored in Postgres)
- [ ] `ProtectedRoute` component — redirects unauthenticated users to login
- [ ] Auth middleware on all API endpoints except `/health` and `/auth/*`
- [ ] Token refresh endpoint — frontend auto-refreshes before expiry
- [ ] Logout — invalidate refresh token in Postgres
- [ ] User model in Postgres (github_id, username, avatar_url, email)

### 4.2 — GitHub Integration
- [ ] REST API client with automatic rate-limit handling (retry + backoff)
- [ ] GraphQL client for batch queries (PRs, reviews, commits)
- [ ] Repository onboarding flow (connect → validate → kick off Celery task)
- [ ] Historical data backfill (paginated, idempotent by event ID)
- [ ] Circuit breaker for GitHub API (fail gracefully when API is down)
- [ ] **(M2)** Webhook receiver with HMAC-SHA256 signature verification
- [ ] **(M2)** Webhook idempotency (processed events table in Postgres/Redis)

### 4.3 — Data Ingestion & Background Jobs
- [ ] Celery + Redis broker for async task processing
- [ ] `ingest_repo` task — full historical backfill (runs in background)
- [ ] `sync_repo` task — incremental fetch since last sync
- [ ] `compute_daily_metrics` task — scheduled daily aggregation
- [ ] `detect_anomalies` task — scheduled anomaly detection
- [ ] SyncJob model in Postgres (status: PENDING/RUNNING/COMPLETED/FAILED, progress %)
- [ ] API returns immediately: `{ status: "ingesting", job_id: "..." }`
- [ ] Frontend polls job status until complete
- [ ] Dead-letter handling for failed tasks (retry 3x, then mark FAILED)
- [ ] **(M2)** Pub/Sub topics + subscriptions for real-time streaming
- [ ] **(M2)** Event processor worker (Pub/Sub subscriber)

### 4.4 — Data Storage — PostgreSQL (App Database)
- [ ] SQLAlchemy 2.0 async ORM with `asyncpg` driver
- [ ] Connection pooling: `pool_size=20`, `max_overflow=10`
- [ ] Alembic migrations (versioned schema changes)
- [ ] Models: `User`, `Repository`, `SyncJob`, `Anomaly`, `RefreshToken`, `ProcessedEvent`
- [ ] Repository pattern for clean data access layer
- [ ] Test database: separate Postgres instance (or in-memory SQLite for unit tests)
- [ ] Environment separation: `devscope_dev` / `devscope_test` / `devscope_prod` databases

### 4.5 — Data Storage — BigQuery (Analytics Warehouse)
- [ ] Tables: `raw_events`, `pull_requests`, `commits`, `reviews`, `daily_metrics`
- [ ] Partitioned by date, clustered by `repo_id`
- [ ] Dataset separation: `devscope_dev` / `devscope_prod`
- [ ] Parameterized queries everywhere (never string-format SQL)
- [ ] Seed script with 90 days of realistic sample data
- [ ] Data retention policies (raw: 90 days, aggregated: unlimited)

### 4.6 — Metric Computation
- [ ] **PR Latency** — time to first review, to approval, to merge (median + p95)
- [ ] **Code Churn** — additions, deletions, net churn, rework ratio
- [ ] **Review Cycles** — review rounds per PR, review turnaround time
- [ ] **Deployment Frequency** — merges to main per day/week
- [ ] **Throughput** — PRs merged per developer per week
- [ ] **Health Score** — weighted composite 0-100
- [ ] Time-windowed aggregations (7d, 30d, 90d, custom)
- [ ] Per-developer and per-repo breakdowns
- [ ] Redis caching for expensive queries (5-min TTL)

### 4.7 — Anomaly Detection
- [ ] **M1: Z-score anomalies** — flag values >2σ from 14-day rolling mean
- [ ] **M1: Severity classification** — >2σ MEDIUM, >3σ HIGH, >4σ CRITICAL
- [ ] **M1: Anomaly types** — latency spike, churn surge, review bottleneck, throughput drop
- [ ] Anomaly records in PostgreSQL (queryable, resolvable)
- [ ] **(M2)** Vertex AI feature engineering (lags, rolling stats, trends)
- [ ] **(M2)** Model training + online prediction endpoint
- [ ] **(M2)** Confidence scores + scheduled retraining

### 4.8 — Stream Processing — M2 Only
- [ ] **(M2)** Apache Beam pipeline for real-time metric aggregation
- [ ] **(M2)** Sliding window computations (1h, 24h, 7d)
- [ ] **(M2)** Tumbling window for daily snapshots
- [ ] **(M2)** Deployed to Cloud Dataflow with autoscaling

### 4.9 — Backend API (FastAPI)
- [ ] **Auth:** `POST /auth/github/callback`, `POST /auth/refresh`, `POST /auth/logout`
- [ ] **Repos:** `POST /repos`, `GET /repos`, `GET /repos/{id}`, `DELETE /repos/{id}`, `POST /repos/{id}/sync`
- [ ] **Metrics:** `GET /metrics?repo_id=&metric=&window=&group_by=`, `GET /metrics/{repo_id}/health`, `GET /metrics/{repo_id}/developers`
- [ ] **Anomalies:** `GET /anomalies?repo_id=&severity=&page=`, `PATCH /anomalies/{id}/resolve`
- [ ] **Jobs:** `GET /jobs/{id}` — poll sync job status
- [ ] **Health:** `GET /health/live` (liveness), `GET /health/ready` (readiness — checks DB + Redis)
- [ ] **(M2):** `POST /webhooks/github`
- [ ] Unified response envelope: `{ data, error, meta: { page, total, request_id } }`
- [ ] Standardized error format: `{ error: { code, message, details } }`
- [ ] Cursor-based pagination on all list endpoints
- [ ] JWT auth middleware on all protected routes
- [ ] Rate limiting via slowapi (100 req/min per user)
- [ ] Input sanitization on all user inputs
- [ ] Correlation ID middleware (X-Request-ID header)
- [ ] CORS configuration (whitelist frontend origins)
- [ ] Graceful shutdown (close DB pool, flush Redis, drain Celery)
- [ ] OpenAPI/Swagger auto-generated docs at `/docs`

### 4.10 — Frontend Dashboard (React/TypeScript)
- [ ] **Login page** — GitHub OAuth redirect button
- [ ] **Protected routing** — redirect to login if no valid JWT
- [ ] **Onboarding** — add repos after first login
- [ ] **Dashboard** — summary cards, 4 interactive charts, date range picker
- [ ] **PR Latency chart** — area chart with median + p95
- [ ] **Code Churn chart** — stacked bar (additions/deletions)
- [ ] **Review Cycles chart** — distribution histogram
- [ ] **Health Score gauge** — SVG radial gauge (0-100)
- [ ] **Repo detail page** — deep dive, developer table, sortable columns
- [ ] **Anomaly feed** — timeline with severity colors, filterable
- [ ] **Settings page** — repo management, account info
- [ ] **Job progress** — poll Celery job status, show progress bar during ingestion
- [ ] Cursor-based pagination component
- [ ] React Query with `refetchInterval: 30000` for near-real-time updates
- [ ] Route-based lazy loading (`React.lazy` + `Suspense`)
- [ ] Dark/light mode toggle (Tailwind `dark:` classes)
- [ ] Loading skeletons, error boundaries, empty states
- [ ] TypeScript strict mode from Day 1
- [ ] Basic accessibility: semantic HTML, ARIA labels on charts, keyboard nav, color contrast

### 4.11 — Deployment & DevOps
- [ ] Backend Dockerfile (multi-stage build)
- [ ] Worker Dockerfile (Celery)
- [ ] `docker-compose.yml`: Postgres + Redis + Backend + Worker + Frontend
- [ ] Cloud Run deployment (backend + worker as separate services)
- [ ] Cloud SQL (Postgres) + Memorystore (Redis) for production
- [ ] GCP Secret Manager for production secrets
- [ ] GitHub Actions CI (lint, type-check, test on PR)
- [ ] GitHub Actions CD (build, push, deploy on merge to main)
- [ ] Dependabot for automated dependency updates
- [ ] Sentry for error tracking
- [ ] Environment separation: dev/test/prod configs
- [ ] Billing alerts at $50, $100, $200, $300

### 4.12 — Code Quality & DX
- [ ] Pre-commit hooks: ruff (format + lint), eslint, prettier, type-check
- [ ] `.editorconfig` for consistent formatting
- [ ] Locked dependencies: `pip-compile` for Python, `package-lock.json` for Node
- [ ] Conventional commits enforced
- [ ] PR template with checklist
- [ ] 70%+ backend test coverage target
- [ ] Test database strategy (separate Postgres for tests)
- [ ] `Makefile` for all common commands

---

## 5. DATABASE SCHEMAS

### 5.1 — PostgreSQL (App Database)

**`users`**
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    github_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    avatar_url TEXT,
    access_token_encrypted TEXT,       -- encrypted GitHub token
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**`repositories`**
```sql
CREATE TABLE repositories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    github_repo_id BIGINT NOT NULL,
    owner VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    full_name VARCHAR(511) NOT NULL,    -- "owner/name"
    default_branch VARCHAR(255) DEFAULT 'main',
    language VARCHAR(100),
    stars INTEGER DEFAULT 0,
    forks INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, github_repo_id)
);
CREATE INDEX idx_repos_user_id ON repositories(user_id);
```

**`sync_jobs`**
```sql
CREATE TABLE sync_jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id UUID REFERENCES repositories(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',  -- PENDING, RUNNING, COMPLETED, FAILED
    job_type VARCHAR(20) NOT NULL,      -- BACKFILL, SYNC
    progress INTEGER DEFAULT 0,          -- 0-100
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_sync_jobs_repo_status ON sync_jobs(repo_id, status);
```

**`anomalies`**
```sql
CREATE TABLE anomalies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    repo_id UUID REFERENCES repositories(id) ON DELETE CASCADE,
    anomaly_type VARCHAR(50) NOT NULL,   -- pr_latency_spike, churn_surge, etc.
    metric_name VARCHAR(50) NOT NULL,
    expected_value DOUBLE PRECISION,
    actual_value DOUBLE PRECISION,
    severity VARCHAR(10) NOT NULL,       -- LOW, MEDIUM, HIGH, CRITICAL
    confidence DOUBLE PRECISION,
    is_resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMPTZ,
    detected_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_anomalies_repo_severity ON anomalies(repo_id, severity);
CREATE INDEX idx_anomalies_detected ON anomalies(detected_at DESC);
```

**`refresh_tokens`**
```sql
CREATE TABLE refresh_tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,    -- SHA-256 hash (never store raw)
    expires_at TIMESTAMPTZ NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX idx_refresh_tokens_hash ON refresh_tokens(token_hash);
```

**`processed_events`** (for idempotency)
```sql
CREATE TABLE processed_events (
    event_id VARCHAR(255) PRIMARY KEY,   -- GitHub event delivery ID
    event_type VARCHAR(50) NOT NULL,
    processed_at TIMESTAMPTZ DEFAULT NOW()
);
-- Auto-cleanup: DELETE WHERE processed_at < NOW() - INTERVAL '7 days'
```

### 5.2 — BigQuery (Analytics Warehouse)

**`pull_requests`** — partitioned by `created_date`, clustered by `repo_id`
```sql
CREATE TABLE devscope.pull_requests (
    pr_id STRING NOT NULL,
    repo_id STRING NOT NULL,
    number INT64,
    title STRING,
    author STRING,
    state STRING,                        -- open, closed, merged
    created_at TIMESTAMP,
    first_review_at TIMESTAMP,
    approved_at TIMESTAMP,
    merged_at TIMESTAMP,
    closed_at TIMESTAMP,
    additions INT64,
    deletions INT64,
    changed_files INT64,
    review_rounds INT64,
    created_date DATE                    -- partition column
)
PARTITION BY created_date
CLUSTER BY repo_id;
```

**`commits`** — partitioned by `committed_date`, clustered by `repo_id`
```sql
CREATE TABLE devscope.commits (
    commit_sha STRING NOT NULL,
    repo_id STRING NOT NULL,
    author STRING,
    message STRING,
    committed_at TIMESTAMP,
    additions INT64,
    deletions INT64,
    committed_date DATE
)
PARTITION BY committed_date
CLUSTER BY repo_id;
```

**`reviews`** — clustered by `repo_id`
```sql
CREATE TABLE devscope.reviews (
    review_id STRING NOT NULL,
    pr_id STRING NOT NULL,
    repo_id STRING NOT NULL,
    reviewer STRING,
    state STRING,                        -- APPROVED, CHANGES_REQUESTED, COMMENTED
    submitted_at TIMESTAMP
)
CLUSTER BY repo_id;
```

**`daily_metrics`** — partitioned by `metric_date`, clustered by `repo_id`
```sql
CREATE TABLE devscope.daily_metrics (
    repo_id STRING NOT NULL,
    metric_date DATE NOT NULL,
    metric_name STRING NOT NULL,
    metric_value FLOAT64,
    developer STRING                     -- NULL = repo-level aggregate
)
PARTITION BY metric_date
CLUSTER BY repo_id;
```

---

## 6. API RESPONSE ENVELOPE

Every API response follows this format:

**Success:**
```json
{
    "data": { ... },
    "error": null,
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2026-04-01T12:00:00Z"
    }
}
```

**Success (paginated list):**
```json
{
    "data": [ ... ],
    "error": null,
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2026-04-01T12:00:00Z",
        "pagination": {
            "page": 1,
            "per_page": 20,
            "total": 142,
            "total_pages": 8,
            "next_cursor": "eyJpZCI6IjEyMyJ9"
        }
    }
}
```

**Error:**
```json
{
    "data": null,
    "error": {
        "code": "REPO_NOT_FOUND",
        "message": "Repository with ID abc-123 not found",
        "details": { "repo_id": "abc-123" }
    },
    "meta": {
        "request_id": "req_abc123",
        "timestamp": "2026-04-01T12:00:00Z"
    }
}
```

**Standard error codes:**
```
AUTH_REQUIRED         — No JWT provided
AUTH_INVALID          — JWT expired or invalid
AUTH_FORBIDDEN        — Not authorized for this resource
VALIDATION_ERROR      — Request body/params invalid
REPO_NOT_FOUND        — Repository doesn't exist
JOB_NOT_FOUND         — Sync job doesn't exist
RATE_LIMITED          — Too many requests
GITHUB_API_ERROR      — GitHub API failed
BIGQUERY_ERROR        — BigQuery query failed
INTERNAL_ERROR        — Unexpected server error
```

---

## 7. WEEK-BY-WEEK BUILD PLAN

---

### ═══════════════════════════════════════════════════════
### MILESTONE 1 — "DevScope Core" (Weeks 1–4)
### ═══════════════════════════════════════════════════════

---

### WEEK 1 — FOUNDATION
**Goal:** Project scaffolded, GCP configured, Postgres + BigQuery set up, GitHub client built, basic data flowing.

**Deliverable by Friday:** You can run a script that pulls PR data from any public GitHub repo, stores it in both Postgres and BigQuery, and query it.

---

#### Day 1 (Mon): Project Scaffolding + Tooling
**Focus: Set up everything that every future day depends on. Do it right once.**

**Morning — Project Init (3 hours)**
- [ ] Create GitHub repo: `devscope`
- [ ] Create the full directory structure (Section 3 above)
- [ ] Initialize backend:
  - `pyproject.toml` with project metadata
  - `requirements.in`: fastapi, uvicorn[standard], httpx, sqlalchemy[asyncio], asyncpg, alembic, google-cloud-bigquery, redis, celery, pyjwt, pydantic-settings, python-dotenv, sentry-sdk[fastapi], slowapi
  - `requirements-dev.in`: pytest, pytest-asyncio, pytest-cov, ruff, mypy, factory-boy, httpx (for TestClient)
  - Generate locked files: `pip-compile requirements.in > requirements.txt`
  - Virtual environment: `python -m venv venv && source venv/bin/activate`
- [ ] Initialize frontend:
  - `npm create vite@latest frontend -- --template react-ts`
  - Install: `npm i tailwindcss @tailwindcss/vite react-router-dom @tanstack/react-query recharts axios`
  - Install dev: `npm i -D eslint prettier eslint-config-prettier @types/react`
  - Configure Tailwind with Vite plugin
  - Set `tsconfig.json` → `"strict": true`
- [ ] Commit `package-lock.json` (never `.gitignore` it)

**Afternoon — DX Tooling (2 hours)**
- [ ] Create `.editorconfig`:
  ```ini
  root = true
  [*]
  indent_style = space
  indent_size = 2
  end_of_line = lf
  charset = utf-8
  trim_trailing_whitespace = true
  insert_final_newline = true
  [*.py]
  indent_size = 4
  ```
- [ ] Create `.pre-commit-config.yaml`:
  ```yaml
  repos:
    - repo: https://github.com/astral-sh/ruff-pre-commit
      rev: v0.4.4
      hooks:
        - id: ruff
          args: [--fix]
        - id: ruff-format
    - repo: https://github.com/pre-commit/mirrors-eslint
      rev: v8.56.0
      hooks:
        - id: eslint
  ```
  - Install: `pip install pre-commit && pre-commit install`
- [ ] Create `.prettierrc`, `ruff.toml` (line-length: 100, target: py311)
- [ ] Create `.env.example` with all variables (Section 10)
- [ ] Create `.env.dev` (committed — dev defaults, no real secrets)
- [ ] Create `Makefile` (Section 11)
- [ ] Create `.gitignore` (Python + Node + GCP + `.env` but NOT `.env.dev`)
- [ ] Enable Dependabot: `.github/dependabot.yml`
- [ ] Write initial `README.md`
- [ ] **Commit:** `chore: initialize project with tooling, linting, pre-commit, and locked deps`

**Evening — Verify (1 hour)**
- [ ] `pre-commit run --all-files` passes
- [ ] Backend virtual env works, imports resolve
- [ ] Frontend `npm run dev` starts without errors
- [ ] **Commit:** `chore: verify dev environment setup`

**🧠 Learning Focus:** pip-compile, pre-commit hooks, EditorConfig, TypeScript strict mode
**⚠️ Blockers:** pre-commit Python version mismatch — ensure hooks match your Python version

---

#### Day 2 (Tue): GCP Setup + PostgreSQL + Docker Compose
**Focus: Get both databases running locally and in GCP.**

**Morning — GCP Setup (2–3 hours)**
- [ ] Create GCP project (or use existing)
- [ ] Enable APIs: BigQuery, Cloud Run, Artifact Registry, Cloud SQL Admin, Secret Manager
  - Skip Pub/Sub, Dataflow, Vertex AI — that's Milestone 2
- [ ] Create service account with roles: BigQuery Admin, Cloud Run Admin, Secret Manager Accessor, Cloud SQL Client
- [ ] Download service account JSON key → add to `.env` (NOT committed)
- [ ] Install `gcloud` CLI, authenticate, set project
- [ ] Test BigQuery connection from Python: run a simple query
- [ ] Set up billing alerts: $50, $100, $200, $300

**Afternoon — Docker Compose + Postgres (3 hours)**
- [ ] Write `infra/docker-compose.yml`:
  ```yaml
  services:
    postgres:
      image: postgres:16-alpine
      environment:
        POSTGRES_USER: devscope
        POSTGRES_PASSWORD: devscope_local
        POSTGRES_DB: devscope_dev
      ports: ["5432:5432"]
      volumes: [postgres_data:/var/lib/postgresql/data]

    redis:
      image: redis:7-alpine
      ports: ["6379:6379"]

  volumes:
    postgres_data:
  ```
- [ ] Run `docker compose up -d` — verify Postgres and Redis start
- [ ] Connect to Postgres: `psql -h localhost -U devscope devscope_dev`
- [ ] Test Redis: `redis-cli ping` → PONG
- [ ] Build `backend/app/config.py` with pydantic-settings:
  ```python
  class Settings(BaseSettings):
      ENVIRONMENT: str = "development"  # development | test | production
      DATABASE_URL: str = "postgresql+asyncpg://devscope:devscope_local@localhost:5432/devscope_dev"
      REDIS_URL: str = "redis://localhost:6379/0"
      # ... all other settings
      model_config = SettingsConfigDict(env_file=".env")
  ```
- [ ] Build `backend/app/db/engine.py`:
  ```python
  engine = create_async_engine(
      settings.DATABASE_URL,
      pool_size=20,
      max_overflow=10,
      pool_pre_ping=True,     # detect stale connections
      pool_recycle=3600,       # recycle connections every hour
  )
  async_session = async_sessionmaker(engine, expire_on_commit=False)
  ```
- [ ] Build `backend/app/core/redis_client.py`:
  ```python
  redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)

  async def cache_get(key: str) -> str | None
  async def cache_set(key: str, value: str, ttl: int = 300) -> None
  async def cache_delete(key: str) -> None
  ```

**Evening — Alembic + Initial Migration (1–2 hours)**
- [ ] Initialize Alembic: `alembic init migrations`
- [ ] Configure `alembic.ini` and `env.py` for async SQLAlchemy
- [ ] Build `backend/app/db/models.py` — User, Repository, SyncJob, Anomaly, RefreshToken, ProcessedEvent
- [ ] Create first migration: `alembic revision --autogenerate -m "initial schema"`
- [ ] Run migration: `alembic upgrade head`
- [ ] Verify tables in Postgres
- [ ] **Commit:** `feat(infra): add docker-compose, Postgres with Alembic migrations, and Redis`

**🧠 Learning Focus:** Docker Compose, SQLAlchemy 2.0 async, Alembic migrations, connection pooling
**⚠️ Blockers:** asyncpg requires `postgresql+asyncpg://` URI scheme (not `postgresql://`). Alembic async setup is tricky — follow the [official async recipe](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic).

---

#### Day 3 (Wed): BigQuery Schemas + Client
**Focus: Design analytics tables and build reliable BigQuery operations.**

**Morning — BigQuery Setup (2–3 hours)**
- [ ] Create BigQuery datasets: `devscope_dev` and `devscope_prod`
- [ ] Create tables (Section 5.2): `pull_requests`, `commits`, `reviews`, `daily_metrics`
- [ ] Verify partitioning and clustering in BigQuery Console

**Afternoon — BigQuery Client (3 hours)**
- [ ] Build `backend/app/core/bigquery_client.py`:
  ```python
  class BigQueryClient:
      def __init__(self, project_id: str, dataset: str):
          self.client = bigquery.Client(project=project_id)
          self.dataset = dataset

      async def insert_rows(self, table: str, rows: list[dict]) -> None
          # Streaming insert with batch size limit (500 rows)
      async def query(self, sql: str, params: dict) -> list[dict]
          # Parameterized query
      async def table_exists(self, table: str) -> bool
  ```
- [ ] All queries use parameterized syntax: `WHERE repo_id = @repo_id`
- [ ] Batch inserts: split into chunks of 500 rows
- [ ] Environment-aware: reads `BQ_DATASET` from config (`devscope_dev` vs `devscope_prod`)
- [ ] Error handling: wrap BigQuery exceptions with custom error types

**Evening — Seed Script (1 hour)**
- [ ] Build `scripts/seed_data.py`:
  - Generate 90 days of data for 3 sample repos
  - 50-100 PRs per repo with realistic distributions
  - Include anomalous periods (latency spikes on day 30, 60)
  - Insert into BigQuery
- [ ] Run and verify data in BigQuery Console
- [ ] **Commit:** `feat(backend): add BigQuery schemas, client, and seed data script`

**🧠 Learning Focus:** BigQuery partitioning/clustering, parameterized queries, streaming inserts

---

#### Day 4 (Thu): GitHub API Client
**Focus: Build a robust, well-tested GitHub API wrapper with resilience patterns.**

**Morning — Core Client (3 hours)**
- [ ] Build `backend/app/core/github_client.py`:
  ```python
  class GitHubClient:
      async def get_repo(owner, name) -> dict
      async def list_pull_requests(owner, name, state, per_page, page) -> list[dict]
      async def get_pull_request(owner, name, number) -> dict
      async def list_commits(owner, name, since, until) -> list[dict]
      async def list_reviews(owner, name, pr_number) -> list[dict]
      async def paginate_all(url, params) -> list[dict]  # follows Link headers
  ```
- [ ] Use `httpx.AsyncClient` with connection pooling
- [ ] Parse `Link` header for pagination
- [ ] Rate limit detection: check `X-RateLimit-Remaining` and `X-RateLimit-Reset`
- [ ] Pre-request check: sleep until reset if remaining < 10

**Afternoon — Resilience (2 hours)**
- [ ] Build `backend/app/utils/circuit_breaker.py`:
  ```python
  class CircuitBreaker:
      # States: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing)
      # After 5 consecutive failures → OPEN for 60 seconds
      # Then HALF_OPEN: let one request through to test
      async def call(self, func, *args, **kwargs)
  ```
- [ ] Add exponential backoff retry: 3 retries with 1s, 2s, 4s delays
- [ ] Custom exceptions: `GitHubRateLimited`, `GitHubNotFound`, `GitHubUnavailable`
- [ ] Structured logging on every API call: method, URL, status, rate limit remaining

**Evening — Input Sanitization + Testing (2 hours)**
- [ ] Build `backend/app/utils/sanitizer.py`:
  ```python
  def sanitize_repo_name(name: str) -> str:
      # Strip HTML, validate against GitHub naming rules
      # Only allow: alphanumeric, hyphens, underscores, dots
  ```
- [ ] Unit tests with mocked HTTP (use `httpx.MockTransport`)
- [ ] Test: success, pagination, rate limit, circuit breaker triggers, invalid input
- [ ] **Commit:** `feat(backend): add GitHub API client with rate limiting, circuit breaker, and tests`

**🧠 Learning Focus:** httpx async, circuit breaker pattern, retry with backoff, input validation

---

#### Day 5 (Fri): Ingestion Service + Celery
**Focus: Build the data pipeline that moves GitHub data into both databases.**

**Morning — Celery Setup (2 hours)**
- [ ] Build `backend/workers/celery_app.py`:
  ```python
  celery = Celery('devscope')
  celery.config_from_object({
      'broker_url': settings.REDIS_URL,
      'result_backend': settings.REDIS_URL,
      'task_serializer': 'json',
      'task_acks_late': True,           # re-deliver if worker crashes
      'task_reject_on_worker_lost': True,
      'worker_prefetch_multiplier': 1,  # one task at a time per worker
  })
  ```
- [ ] Add `celery` to `docker-compose.yml` as a worker service
- [ ] Test: submit a dummy task, verify it runs

**Afternoon — Ingestion Service + Tasks (3 hours)**
- [ ] Build `backend/app/services/ingestion_service.py`:
  ```python
  class IngestionService:
      async def onboard_repo(user_id, owner, name) -> Repository:
          # 1. Validate repo exists on GitHub
          # 2. Sanitize inputs
          # 3. Create Repository record in Postgres
          # 4. Create SyncJob record (status: PENDING)
          # 5. Dispatch Celery task
          # 6. Return repo + job_id immediately

      async def backfill_repo(job_id, repo_id) -> None:
          # 1. Update SyncJob status → RUNNING
          # 2. Fetch all PRs (paginated) from GitHub
          # 3. For each PR: fetch reviews
          # 4. Fetch commits (last 90 days)
          # 5. Transform → BigQuery format
          # 6. Batch insert into BigQuery
          # 7. Update progress % in SyncJob (Postgres)
          # 8. Update SyncJob status → COMPLETED
          # 9. Update repo.last_synced_at

      async def sync_repo(job_id, repo_id) -> None:
          # Incremental: only since last_synced_at
  ```
- [ ] Build `backend/workers/tasks/ingestion_tasks.py`:
  ```python
  @celery.task(bind=True, max_retries=3)
  def ingest_repo_task(self, job_id: str, repo_id: str):
      # Calls ingestion_service.backfill_repo()
      # On failure: update SyncJob → FAILED with error message
  ```
- [ ] Idempotent inserts: check `processed_events` table before writing to BigQuery

**Evening — Test E2E (1–2 hours)**
- [ ] Start Postgres + Redis + Backend + Worker (`docker compose up`)
- [ ] Manually call ingestion on a small public repo
- [ ] Watch Celery logs — verify tasks process
- [ ] Check Postgres: repo record + sync job record
- [ ] Check BigQuery: PR + commit data
- [ ] **Commit:** `feat(backend): add Celery task queue and ingestion pipeline`

**🧠 Learning Focus:** Celery task patterns, async workers, dual-database writes, idempotency

---

#### Day 6 (Sat): Structured Logging + Error Tracking
**Focus: Observability infrastructure that you'll rely on for the rest of the project.**

**Morning — Structured Logging + Correlation IDs (2 hours)**
- [ ] Build `backend/app/utils/logger.py`:
  ```python
  import structlog
  structlog.configure(
      processors=[
          structlog.processors.add_log_level,
          structlog.processors.TimeStamper(fmt="iso"),
          structlog.processors.JSONRenderer()
      ]
  )
  ```
- [ ] Build `backend/app/api/middleware/correlation_id.py`:
  ```python
  @app.middleware("http")
  async def correlation_id_middleware(request, call_next):
      request_id = request.headers.get("X-Request-ID", str(uuid4()))
      # Bind to structlog context
      # Add to response headers
  ```
- [ ] All log lines include: `request_id`, `user_id` (if authed), `endpoint`, `method`

**Afternoon — Sentry + Error Handler (2 hours)**
- [ ] Sign up for Sentry (free tier: 5K events/month)
- [ ] Integrate: `sentry_sdk.init(dsn=settings.SENTRY_DSN, traces_sample_rate=0.1)`
- [ ] Build `backend/app/api/middleware/error_handler.py`:
  ```python
  # Catches all exceptions, returns standardized error envelope
  # Maps known exceptions to error codes:
  #   RepositoryNotFound → 404, REPO_NOT_FOUND
  #   GitHubRateLimited → 503, GITHUB_API_ERROR
  #   ValidationError → 422, VALIDATION_ERROR
  #   Unexpected → 500, INTERNAL_ERROR (logged to Sentry)
  ```
- [ ] Build `backend/app/models/envelope.py`:
  ```python
  class APIResponse(BaseModel, Generic[T]):
      data: T | None = None
      error: APIError | None = None
      meta: ResponseMeta
  ```

**Evening — Test Logging + Sentry**
- [ ] Trigger an error → verify it appears in Sentry dashboard
- [ ] Make a request → verify correlation ID in logs and response header
- [ ] **Commit:** `feat(backend): add structured logging, correlation IDs, Sentry, and error envelope`

**🧠 Learning Focus:** structlog, correlation ID pattern, Sentry integration, error handling middleware

---

#### Day 7 (Sun): Week 1 Review + Catch-Up
- [ ] Review all code — resolve TODO comments
- [ ] Run full test suite, fix failures
- [ ] Run `pre-commit run --all-files` — everything clean
- [ ] Write `DEV_LOG.md` Week 1 entry
- [ ] Update `README.md` with current setup instructions
- [ ] **Commit:** `docs: add Week 1 dev log and setup instructions`
- [ ] **Push everything**

**Week 1 Checkpoint:**
```
✅ Project scaffolded with pre-commit, locked deps, editorconfig, strict TS
✅ Docker Compose: Postgres + Redis running locally
✅ PostgreSQL schemas + Alembic migrations (6 tables)
✅ BigQuery schemas (4 tables, partitioned + clustered)
✅ GitHub API client with rate limiting + circuit breaker
✅ Celery task queue with Redis broker
✅ Ingestion pipeline: GitHub → Postgres + BigQuery (via Celery worker)
✅ Structured logging with correlation IDs
✅ Sentry error tracking
✅ Input sanitization
```

---

### WEEK 2 — BACKEND API + AUTH + FRONTEND SHELL
**Goal:** Complete FastAPI with auth, all endpoints, rate limiting. React app with login, routing, repo onboarding.

**Deliverable by Friday:** You can log in with GitHub, onboard repos through the UI, see ingestion progress, and view repo list — all authenticated.

---

#### Day 8 (Mon): Authentication — GitHub OAuth + JWT
**Focus: Real auth that protects everything.**

**Morning — GitHub OAuth Flow (3 hours)**
- [ ] Register GitHub OAuth App (Settings → Developer Settings → OAuth Apps)
  - Callback URL: `http://localhost:8000/api/v1/auth/github/callback`
- [ ] Build `backend/app/services/auth_service.py`:
  ```python
  class AuthService:
      async def get_github_auth_url() -> str
          # Returns GitHub OAuth authorize URL with client_id + scope

      async def handle_github_callback(code: str) -> TokenPair:
          # 1. Exchange code for GitHub access token
          # 2. Fetch user profile from GitHub API
          # 3. Upsert user in Postgres (create or update)
          # 4. Store encrypted GitHub token
          # 5. Generate JWT access token (15-min expiry)
          # 6. Generate refresh token (7-day, stored hashed in Postgres)
          # 7. Return { access_token, refresh_token, user }

      async def refresh_tokens(refresh_token: str) -> TokenPair:
          # 1. Hash the token, look up in Postgres
          # 2. Verify not expired, not revoked
          # 3. Revoke old refresh token
          # 4. Issue new access + refresh tokens

      async def logout(refresh_token: str) -> None:
          # Revoke refresh token in Postgres
  ```

**Afternoon — JWT Middleware (2 hours)**
- [ ] Build `backend/app/api/middleware/auth.py`:
  ```python
  async def get_current_user(
      authorization: str = Header(...)
  ) -> User:
      # 1. Extract Bearer token
      # 2. Decode JWT, verify signature + expiry
      # 3. Load user from Postgres by user_id in token
      # 4. Return User or raise AUTH_INVALID
  ```
- [ ] Build auth endpoints:
  - `GET /api/v1/auth/github` — returns auth URL
  - `GET /api/v1/auth/github/callback` — handles callback, returns tokens
  - `POST /api/v1/auth/refresh` — refresh token pair
  - `POST /api/v1/auth/logout` — revoke refresh token

**Evening — Test Auth Flow (1–2 hours)**
- [ ] Test with curl: get auth URL → open in browser → callback → receive tokens
- [ ] Test protected endpoint with/without JWT
- [ ] Test token refresh
- [ ] Write unit tests for auth_service (mock GitHub API calls)
- [ ] **Commit:** `feat(backend): add GitHub OAuth login with JWT auth and refresh tokens`

**🧠 Learning Focus:** OAuth2 authorization code flow, JWT structure (header.payload.signature), token refresh patterns

---

#### Day 9 (Tue): FastAPI Endpoints — Repos + Jobs
**Focus: Build all CRUD endpoints with proper pagination, auth, and response envelopes.**

**Morning — Repo Endpoints (3 hours)**
- [ ] Build Pydantic schemas (`models/schemas.py`):
  ```python
  class RepoCreate(BaseModel):
      owner: str = Field(max_length=255, pattern=r'^[a-zA-Z0-9._-]+$')
      name: str = Field(max_length=255, pattern=r'^[a-zA-Z0-9._-]+$')

  class RepoResponse(BaseModel):
      id: str
      full_name: str
      language: str | None
      stars: int
      last_synced_at: datetime | None
      is_active: bool
      current_job: SyncJobBrief | None

  class PaginatedResponse(BaseModel, Generic[T]):
      items: list[T]
      pagination: PaginationMeta
  ```
- [ ] Build DB repositories (`db/repositories/repo_repo.py`):
  ```python
  class RepoRepository:
      async def create(session, user_id, data) -> Repository
      async def get_by_id(session, repo_id, user_id) -> Repository | None
      async def list_for_user(session, user_id, cursor, limit) -> tuple[list, str|None]
      async def soft_delete(session, repo_id, user_id) -> None
  ```
- [ ] Implement endpoints (all wrapped in response envelope):
  - `POST /api/v1/repos` — validate, create, dispatch Celery task
  - `GET /api/v1/repos?cursor=&limit=20` — paginated list for current user
  - `GET /api/v1/repos/{id}` — detail with current job status
  - `DELETE /api/v1/repos/{id}` — soft delete
  - `POST /api/v1/repos/{id}/sync` — trigger incremental sync

**Afternoon — Job Status + Rate Limiting (2 hours)**
- [ ] Build `GET /api/v1/jobs/{id}` — returns sync job status + progress
- [ ] Add rate limiting via slowapi:
  ```python
  limiter = Limiter(key_func=get_user_id_from_jwt)

  @router.get("/repos")
  @limiter.limit("100/minute")
  async def list_repos(...):
  ```
- [ ] Build health endpoints:
  - `GET /api/v1/health/live` — always returns 200 (process is alive)
  - `GET /api/v1/health/ready` — checks Postgres + Redis + BigQuery connections

**Evening — Graceful Shutdown + Tests (2 hours)**
- [ ] Add lifespan handler to FastAPI:
  ```python
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # STARTUP: init DB pool, Redis, Sentry
      yield
      # SHUTDOWN: close DB pool, close Redis, flush Sentry
      await engine.dispose()
      await redis.close()
  ```
- [ ] Write integration tests with TestClient + test database
- [ ] **Commit:** `feat(backend): add repo CRUD, job status, rate limiting, and graceful shutdown`

**🧠 Learning Focus:** Cursor-based pagination, repository pattern, FastAPI lifespan, rate limiting

---

#### Day 10 (Wed): Frontend — Auth + Layout + Routing
**Focus: Build the React shell with real authentication.**

**Morning — Auth Flow (3 hours)**
- [ ] Build `frontend/src/store/auth.ts` (React Context):
  ```typescript
  interface AuthState {
      user: User | null;
      accessToken: string | null;
      isAuthenticated: boolean;
      login: () => void;        // redirect to GitHub OAuth
      handleCallback: (code: string) => Promise<void>;
      logout: () => void;
      refreshToken: () => Promise<void>;
  }
  ```
- [ ] Build `Login.tsx` — "Sign in with GitHub" button → redirects to OAuth URL
- [ ] Build callback handler — exchanges code for tokens, stores in memory (NOT localStorage)
- [ ] Build `ProtectedRoute.tsx` — redirects to `/login` if not authenticated
- [ ] Auto-refresh: set timer to refresh tokens before 15-min expiry
- [ ] Add Authorization header to Axios interceptor:
  ```typescript
  client.interceptors.request.use((config) => {
      const token = authStore.accessToken;
      if (token) config.headers.Authorization = `Bearer ${token}`;
      return config;
  });
  ```

**Afternoon — Layout + Routing (3 hours)**
- [ ] Set up routing with lazy loading:
  ```typescript
  const Dashboard = lazy(() => import('./pages/Dashboard'));
  const RepoDetail = lazy(() => import('./pages/RepoDetail'));
  const Anomalies = lazy(() => import('./pages/Anomalies'));

  <Suspense fallback={<LoadingSpinner />}>
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="/" element={<Dashboard />} />
          <Route path="/repos/:repoId" element={<RepoDetail />} />
          <Route path="/anomalies" element={<Anomalies />} />
          <Route path="/settings" element={<Settings />} />
        </Route>
      </Route>
    </Routes>
  </Suspense>
  ```
- [ ] Build `DashboardLayout.tsx` — sidebar + header + content area
- [ ] Build `Sidebar.tsx` — nav links with active state (NavLink), anomaly badge placeholder
- [ ] Build `Header.tsx` — app name, user avatar from GitHub, logout button
- [ ] Style with Tailwind — dark sidebar, light content

**Evening — API Client Layer**
- [ ] Build `api/client.ts` — Axios instance with error envelope parsing:
  ```typescript
  // Response interceptor: unwrap envelope
  client.interceptors.response.use(
      (res) => res.data,  // returns { data, error, meta }
      (err) => {
          const apiError = err.response?.data?.error;
          if (apiError?.code === 'AUTH_INVALID') authStore.refreshToken();
          return Promise.reject(apiError || err);
      }
  );
  ```
- [ ] Build `api/repos.ts`, `api/auth.ts`
- [ ] Build `useRepos.ts` hook with React Query
- [ ] **Commit:** `feat(frontend): add GitHub OAuth login, protected routing, and dashboard layout`

**🧠 Learning Focus:** OAuth frontend flow, React Context for auth, Axios interceptors, React.lazy code splitting

---

#### Day 11 (Thu): Frontend — Repo Onboarding + Job Polling
**Focus: Complete the onboarding UX with background job progress.**

**Morning — Onboarding Flow (3 hours)**
- [ ] Build `Onboarding.tsx` / `AddRepoModal.tsx`:
  - Form: owner + repo name inputs (validated)
  - Submit → POST /repos → receive job_id
  - Show progress bar polling GET /jobs/{id} every 2 seconds
  - On complete: invalidate repos query, show success
  - On failure: show error message with retry option
- [ ] Build `RepoCard.tsx`:
  - Repo name, language badge, stars, last synced
  - Status indicator: green (synced), yellow (syncing), red (failed)
  - Click → navigate to `/repos/:id`
- [ ] Build `RepoList.tsx`:
  - Grid of RepoCards
  - "Add Repository" button → opens modal
  - Empty state: "No repos yet — add one to get started"
  - Pagination component at bottom

**Afternoon — Common Components (2 hours)**
- [ ] Build `LoadingSpinner.tsx` — skeleton loaders for cards and pages
- [ ] Build `ErrorBoundary.tsx` — catch React errors, show "Something went wrong" + retry
- [ ] Build `Pagination.tsx` — reusable cursor-based pagination (Previous / Next)
- [ ] Build `EmptyState.tsx` — reusable empty state with icon + message + action

**Evening — Polish + CSP (1 hour)**
- [ ] Add Content Security Policy meta tag to `index.html`:
  ```html
  <meta http-equiv="Content-Security-Policy"
    content="default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';
    img-src 'self' https://avatars.githubusercontent.com; connect-src 'self' http://localhost:8000">
  ```
- [ ] Test full flow: login → add repo → see progress → repo appears in list
- [ ] **Commit:** `feat(frontend): add repo onboarding with job progress polling`

**🧠 Learning Focus:** Polling patterns with React Query, progressive UX for long-running operations

---

#### Day 12 (Fri): Redis Caching + API Polish
**Focus: Add caching layer and finalize all API details.**

**Morning — Redis Caching (2 hours)**
- [ ] Add caching to metrics (will be built next week, prep the pattern now):
  ```python
  async def get_cached_or_compute(key: str, compute_fn, ttl: int = 300):
      cached = await redis.get(key)
      if cached:
          return json.loads(cached)
      result = await compute_fn()
      await redis.set(key, json.dumps(result), ex=ttl)
      return result
  ```
- [ ] Cache repo list for each user (1-min TTL, invalidate on repo create/delete)
- [ ] Cache GitHub repo metadata (5-min TTL, reduces API calls)

**Afternoon — API Polish Pass (3 hours)**
- [ ] Verify all endpoints return proper envelope format
- [ ] Verify all error cases return proper error codes
- [ ] Verify pagination works on all list endpoints
- [ ] Verify rate limiting works (test with rapid requests)
- [ ] Verify correlation ID flows through logs
- [ ] Verify CORS allows frontend origin
- [ ] Check Swagger UI at `/docs` — all schemas documented

**Evening — Integration Tests (2 hours)**
- [ ] Set up test database in `conftest.py`:
  ```python
  @pytest.fixture
  async def test_db():
      # Create test database, run migrations, yield session, teardown
  ```
- [ ] Write integration tests for auth flow, repo CRUD, job creation
- [ ] Check coverage: `pytest --cov=app --cov-report=term-missing`
- [ ] **Commit:** `feat(backend): add Redis caching and comprehensive API integration tests`

**🧠 Learning Focus:** Redis caching patterns, cache invalidation, test database setup

---

#### Day 13 (Sat): Week 2 Catch-Up + Buffer
- [ ] Fix any bugs from the week
- [ ] Refactor anything that feels off
- [ ] Write additional tests to improve coverage
- [ ] Update `DEV_LOG.md`

#### Day 14 (Sun): Week 2 Review
- [ ] End-to-end test: login → add repo → data ingests → repo list shows
- [ ] Run full test suite
- [ ] **Push everything**

**Week 2 Checkpoint:**
```
✅ GitHub OAuth2 login with JWT access + refresh tokens
✅ All API endpoints with auth, pagination, rate limiting, error envelopes
✅ Graceful shutdown handling
✅ React app with login, protected routes, lazy loading
✅ Repo onboarding with Celery job progress polling
✅ Redis caching layer
✅ Health checks (liveness + readiness)
✅ Integration tests with test database
```

---

### WEEK 3 — METRICS ENGINE + DASHBOARD
**Goal:** Compute real metrics, build interactive charts, add anomaly detection, complete the dashboard.

**Deliverable by Friday:** Full dashboard with 5 chart types, date filtering, repo detail page, developer breakdown, and anomaly alerts — all with live data.

---

#### Day 15 (Mon): Metric Computation — PR Latency + Throughput
**Morning — Metrics Service + PR Latency (3 hours)**
- [ ] Build `backend/app/services/metrics_service.py`:
  ```python
  class MetricsService:
      async def get_pr_latency(repo_id, window) -> MetricResponse
      async def get_code_churn(repo_id, window) -> MetricResponse
      async def get_review_cycles(repo_id, window) -> MetricResponse
      async def get_throughput(repo_id, window) -> MetricResponse
      async def get_health_score(repo_id) -> HealthScore
      async def get_developer_metrics(repo_id, window) -> list[DeveloperMetrics]
  ```
- [ ] PR Latency SQL (BigQuery):
  ```sql
  SELECT DATE(created_at) as date,
    APPROX_QUANTILES(TIMESTAMP_DIFF(first_review_at, created_at, HOUR), 100)[OFFSET(50)] as median_hours,
    APPROX_QUANTILES(TIMESTAMP_DIFF(first_review_at, created_at, HOUR), 100)[OFFSET(95)] as p95_hours
  FROM pull_requests
  WHERE repo_id = @repo_id AND created_date BETWEEN @start AND @end
    AND first_review_at IS NOT NULL
  GROUP BY date ORDER BY date
  ```
- [ ] Throughput SQL: PRs merged per week

**Afternoon — Wire to API with Caching (2 hours)**
- [ ] Implement `GET /api/v1/metrics?repo_id=&metric=&window=`
- [ ] Add Redis caching: `cache key = metrics:{repo_id}:{metric}:{window}`, TTL 5 min
- [ ] Test queries in BigQuery Console first, then through API
- [ ] **Commit:** `feat(backend): add PR latency and throughput metric computation with caching`

---

#### Day 16 (Tue): Remaining Metrics + Health Score
**Morning — Code Churn + Review Cycles (2 hours)**
- [ ] Code Churn SQL: daily additions/deletions
- [ ] Review Cycles SQL: distribution of review rounds, avg turnaround

**Afternoon — Health Score + Developer Breakdown (3 hours)**
- [ ] Health score formula:
  ```
  score = (0.30 × normalize(latency, lower_better) + 0.25 × normalize(review_time, lower_better) +
           0.20 × normalize(throughput, higher_better) + 0.15 × normalize(review_rounds, lower_better) +
           0.10 × normalize(churn_ratio, lower_better)) × 100
  ```
- [ ] Developer metrics: same queries grouped by `author`
- [ ] Wire all to API endpoints
- [ ] **Commit:** `feat(backend): add code churn, review cycles, health score, and developer metrics`

---

#### Day 17 (Wed): Dashboard Charts
**Morning — Chart Components (3 hours)**
- [ ] Build `useMetrics.ts` hook with React Query:
  ```typescript
  export function useMetric(repoId: string, metric: string, window: string) {
      return useQuery({
          queryKey: ['metrics', repoId, metric, window],
          queryFn: () => fetchMetric(repoId, metric, window),
          staleTime: 5 * 60 * 1000,
          refetchInterval: 30 * 1000,  // poll every 30s for near-real-time
      });
  }
  ```
- [ ] Build `PRLatencyChart.tsx` — Recharts AreaChart (median + p95 lines)
- [ ] Build `CodeChurnChart.tsx` — stacked BarChart (green additions, red deletions)
- [ ] Build `MetricCard.tsx` — summary number + trend arrow

**Afternoon — Dashboard Assembly (3 hours)**
- [ ] Build `ReviewCycleChart.tsx` — bar distribution
- [ ] Build `DateRangePicker.tsx` — preset buttons (7d/30d/90d) + URL param state
- [ ] Build `Dashboard.tsx`:
  - Top row: 4 MetricCards
  - DateRangePicker
  - 2×2 chart grid
  - All charts react to date picker + repo selector
- [ ] Add ARIA labels to all charts for accessibility
- [ ] **Commit:** `feat(frontend): add metric charts and dashboard layout`

---

#### Day 18 (Thu): Repo Detail + Developer Table
**Morning — Repo Detail Page (3 hours)**
- [ ] Build `RepoDetail.tsx`:
  - Header: name, stars, language, last synced, health gauge
  - Tabs: Overview | Developers | Settings
  - Overview: all 4 charts scoped to this repo
- [ ] Build `HealthScoreGauge.tsx` — SVG radial gauge with ARIA label

**Afternoon — Developer Table (2 hours)**
- [ ] Build Developers tab:
  - Table: Developer | PRs Merged | Avg Latency | Avg Churn | Review Rounds
  - Sortable columns (client-side)
  - Pagination
- [ ] Build navigation: Dashboard repo card → RepoDetail, breadcrumbs
- [ ] **Commit:** `feat(frontend): add repo detail page with health gauge and developer breakdown`

---

#### Day 19 (Fri): Anomaly Detection + Alert Feed
**Morning — Z-Score Anomaly Service (3 hours)**
- [ ] Build `backend/app/services/anomaly_service.py`:
  ```python
  class AnomalyService:
      async def detect_anomalies(repo_id) -> list[Anomaly]:
          # For each metric: fetch 30 days, compute 14-day rolling mean + std
          # Flag values > 2σ, classify severity
          # Write to PostgreSQL anomalies table (not BigQuery)
          # Check for duplicates by (repo_id, anomaly_type, detected_at date)

      async def get_anomalies(repo_id, severity, cursor, limit) -> PaginatedResponse
      async def resolve_anomaly(anomaly_id, user_id) -> Anomaly
  ```
- [ ] Build Celery task: `detect_anomalies_task` — runs for all active repos
- [ ] Wire API: `GET /anomalies`, `PATCH /anomalies/{id}/resolve`

**Afternoon — Anomaly Frontend (3 hours)**
- [ ] Build `useAnomalies.ts` hook
- [ ] Build `AnomalyTimeline.tsx`:
  - Cards with severity color (red/orange/yellow)
  - Type, metric, expected vs actual, detected timestamp
  - "Resolve" button
- [ ] Build `Anomalies.tsx` page — filterable feed
- [ ] Add anomaly count badge to Sidebar
- [ ] Add anomaly count to Dashboard MetricCards
- [ ] **Commit:** `feat: add statistical anomaly detection and alert feed UI`

---

#### Day 20 (Sat): Week 3 Polish
- [ ] Full E2E walkthrough: login → add repo → metrics load → anomalies show
- [ ] Fix visual bugs, chart edge cases
- [ ] Keyboard navigation check on all interactive elements
- [ ] Color contrast check on anomaly severity colors
- [ ] **Commit:** `fix: Week 3 UI polish and accessibility improvements`

#### Day 21 (Sun): Week 3 Review
- [ ] Run test suite, check coverage target (70%+ backend)
- [ ] Update `DEV_LOG.md`
- [ ] **Push everything**

**Week 3 Checkpoint:**
```
✅ 5 metric computations with BigQuery SQL + Redis caching
✅ 5 interactive Recharts components with date filtering
✅ Dashboard overview with MetricCards + chart grid
✅ Repo detail page with developer table
✅ Health score gauge (SVG)
✅ Z-score anomaly detection with Celery scheduling
✅ Anomaly feed page with severity filtering + resolve
✅ Near-real-time polling (30s refetch interval)
✅ ARIA labels and basic accessibility on all components
```

---

### WEEK 4 — DEPLOY + POLISH (Milestone 1 Complete)
**Goal:** Dockerize, deploy to Cloud Run with Cloud SQL + Memorystore, CI/CD, dark mode, docs. End with a live URL.

---

#### Day 22 (Mon): Docker + Production Build
**Morning — Dockerfiles (3 hours)**
- [ ] `backend/Dockerfile` (multi-stage):
  ```dockerfile
  FROM python:3.11-slim AS builder
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .

  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /app .
  EXPOSE 8000
  HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:8000/api/v1/health/live || exit 1
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] `backend/Dockerfile.worker`:
  ```dockerfile
  FROM python:3.11-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["celery", "-A", "workers.celery_app", "worker", "--loglevel=info"]
  ```
- [ ] Update `docker-compose.yml` with backend + worker services
- [ ] Build frontend → copy dist into backend for static serving
- [ ] Test full app from Docker: `docker compose up --build`

**Afternoon — Production Config (2 hours)**
- [ ] Create `.env.production` template (no secrets — those go in Secret Manager)
- [ ] Update `config.py`: use Secret Manager in production, `.env` in dev
- [ ] Test with `ENVIRONMENT=production` flag
- [ ] **Commit:** `chore(infra): add Docker multi-stage builds and production config`

---

#### Day 23 (Tue): Cloud Run + Cloud SQL + Memorystore
**Morning — GCP Production Resources (3 hours)**
- [ ] Create Cloud SQL Postgres instance (smallest tier)
- [ ] Create Memorystore Redis instance (basic tier)
- [ ] Run Alembic migrations against Cloud SQL
- [ ] Push Docker images to Artifact Registry
- [ ] Deploy backend to Cloud Run:
  - Connect to Cloud SQL via unix socket
  - Connect to Memorystore via VPC connector
  - Set env vars via Secret Manager references

**Afternoon — Deploy Worker + Verify (3 hours)**
- [ ] Deploy Celery worker as separate Cloud Run service (always-on min instances: 1)
- [ ] Test live URL — full flow works
- [ ] Fix CORS for production domain
- [ ] **Commit:** `chore(infra): deploy to Cloud Run with Cloud SQL and Memorystore`

---

#### Day 24 (Wed): CI/CD + Dependabot
**Morning — CI Pipeline (2 hours)**
- [ ] `.github/workflows/ci.yml`:
  - Trigger on PR
  - Backend: ruff check, pytest (with Postgres service container), coverage check
  - Frontend: eslint, type-check

**Afternoon — CD Pipeline (3 hours)**
- [ ] `.github/workflows/cd.yml`:
  - Trigger on merge to main
  - Build Docker images, push to Artifact Registry
  - Deploy to Cloud Run
- [ ] Add GCP credentials as GitHub secret
- [ ] Test: merge a PR → auto-deploy
- [ ] Add CI/CD badges to README
- [ ] Enable branch protection: require CI to pass
- [ ] **Commit:** `ci: add GitHub Actions CI/CD with auto-deploy`

---

#### Day 25 (Thu): Dark Mode + Accessibility
**Morning — Dark Mode (2 hours)**
- [ ] Theme toggle in Header (store preference in cookie, not localStorage)
- [ ] Tailwind `dark:` classes on all components
- [ ] Chart color schemes for both themes

**Afternoon — Accessibility Pass (3 hours)**
- [ ] Semantic HTML: use `<nav>`, `<main>`, `<section>`, `<article>` correctly
- [ ] Keyboard navigation: all interactive elements focusable, proper tab order
- [ ] ARIA labels on charts: `role="img"`, `aria-label="PR latency chart showing..."`
- [ ] Color contrast: verify with Chrome DevTools accessibility audit
- [ ] Skip-to-content link
- [ ] Focus visible styles
- [ ] **Commit:** `feat(frontend): add dark mode and accessibility improvements`

---

#### Day 26 (Fri): Documentation
**Morning — Technical Docs (3 hours)**
- [ ] `docs/architecture.md` — Mermaid diagram + component descriptions
- [ ] `docs/api-reference.md` — export from Swagger, annotate
- [ ] `docs/data-model.md` — both Postgres + BigQuery schemas
- [ ] `docs/setup-guide.md` — clone to running in 15 minutes

**Afternoon — README + ADRs (2 hours)**
- [ ] Polish README: description, architecture diagram, screenshot, quick start, badges
- [ ] Write ADRs:
  - `001-postgres-plus-bigquery.md`
  - `002-celery-for-background-jobs.md`
  - `003-jwt-auth-with-github-oauth.md`
- [ ] **Commit:** `docs: add architecture, API reference, setup guide, and ADRs`

---

#### Day 27 (Sat): Seed Data + Demo Prep
- [ ] Polish seed script (realistic data, anomalous periods)
- [ ] Fresh setup test: clone → setup → running (follow your own guide)
- [ ] Take screenshots for README
- [ ] Prepare 2-minute verbal demo for interviews

#### Day 28 (Sun): Milestone 1 Release
- [ ] Final code review
- [ ] Run full test suite (70%+ coverage)
- [ ] Update CHANGELOG.md
- [ ] Tag `v1.0.0` with release notes
- [ ] **Push everything**

**🎉 MILESTONE 1 COMPLETE — "DevScope Core"**
```
✅ GitHub OAuth login + JWT auth
✅ PostgreSQL (app data) + BigQuery (analytics) dual-database architecture
✅ Celery + Redis for background task processing
✅ GitHub API client with rate limiting + circuit breaker
✅ Ingestion pipeline with progress tracking
✅ 5 metric computations with Redis caching
✅ FastAPI with pagination, rate limiting, error envelopes, correlation IDs
✅ React dashboard with 5 interactive charts + date filtering
✅ Repo detail + developer breakdown
✅ Z-score anomaly detection + alert feed
✅ Dark/light mode, accessibility, lazy loading
✅ Docker + Cloud Run + Cloud SQL + Memorystore
✅ CI/CD with GitHub Actions
✅ Sentry error tracking
✅ Pre-commit hooks, locked deps, Dependabot
✅ Comprehensive documentation
```

---

### ═══════════════════════════════════════════════════════
### MILESTONE 2 — "DevScope Advanced" (Weeks 5–6)
### ═══════════════════════════════════════════════════════

---

### WEEK 5 — REAL-TIME PIPELINE
**Goal:** GitHub webhooks → Pub/Sub → Dataflow → BigQuery in real-time.

---

#### Day 29 (Mon): Pub/Sub Setup + Publisher
- [ ] Enable Pub/Sub API, create topics + subscriptions + dead-letter
- [ ] Build `pubsub_publisher.py` with message schema
- [ ] Build subscriber worker
- [ ] **Commit:** `feat(backend): add Pub/Sub publisher and subscriber`

#### Day 30 (Tue): GitHub Webhooks
- [ ] Build webhook endpoint with HMAC-SHA256 verification
- [ ] Webhook idempotency: check `processed_events` table (Postgres or Redis set)
- [ ] Test with ngrok: open PR → webhook → Pub/Sub
- [ ] **Commit:** `feat(backend): add GitHub webhook receiver with idempotency`

#### Day 31 (Wed): Apache Beam — Learning Day
- [ ] Read Beam Programming Guide (PCollections, PTransforms, windowing, triggers)
- [ ] Build and run tutorial pipeline locally with DirectRunner
- [ ] Sketch production pipeline design
- [ ] **Commit:** `docs: add Beam learning notes and pipeline design`

#### Day 32 (Thu): Dataflow Pipeline — Build
- [ ] Build `pipeline.py`: Pub/Sub → parse → validate → window(24h) → aggregate → BigQuery
- [ ] Build custom PTransforms in `transforms.py`
- [ ] Test locally with DirectRunner
- [ ] **Commit:** `feat(pipeline): build Apache Beam streaming pipeline`

#### Day 33 (Fri): Dataflow Deploy + E2E
- [ ] Deploy to Dataflow (DataflowRunner) with autoscaling
- [ ] Full E2E test: PR opened → webhook → Pub/Sub → Dataflow → BigQuery → dashboard
- [ ] Verify <30 second end-to-end latency
- [ ] **Commit:** `feat(pipeline): deploy Dataflow and verify real-time flow`

#### Day 34 (Sat): Dual-Mode + Fallback
- [ ] Graceful degradation: batch fallback if Dataflow is down
- [ ] Both paths idempotent to same BigQuery tables
- [ ] Update deployment docs
- [ ] **Commit:** `feat: add dual-mode ingestion with graceful degradation`

#### Day 35 (Sun): Week 5 Review + Buffer
- [ ] Bug fixes, refactoring
- [ ] Update `DEV_LOG.md`
- [ ] **Push everything**

---

### WEEK 6 — ML ANOMALY DETECTION + FINAL POLISH
**Goal:** Vertex AI replaces z-scores, dashboard upgraded, v2.0 shipped.

---

#### Day 36 (Mon): Feature Engineering
- [ ] Build `preprocessing.py`: lag features, rolling stats, day-of-week encoding, trends
- [ ] Export training dataset to Cloud Storage
- [ ] **Commit:** `feat(ml): add feature engineering pipeline`

#### Day 37 (Tue): Model Training
- [ ] Train with Vertex AI AutoML or custom IsolationForest
- [ ] Evaluate: precision, recall, F1 vs z-score baseline
- [ ] Save model to Vertex AI Model Registry
- [ ] **Commit:** `feat(ml): train anomaly detection model`

#### Day 38 (Wed): Prediction Endpoint + Integration
- [ ] Deploy model to Vertex AI online endpoint
- [ ] Build `vertex_client.py` for predictions
- [ ] Upgrade `anomaly_service.py`: ML predictions with z-score fallback
- [ ] Cloud Scheduler for hourly detection
- [ ] **Commit:** `feat(ml): deploy Vertex AI endpoint and integrate predictions`

#### Day 39 (Thu): Dashboard Upgrades
- [ ] ML confidence scores on anomaly cards
- [ ] "ML-detected" vs "Rule-based" badges
- [ ] Anomaly overlays on charts (Recharts ReferenceArea)
- [ ] Auto-refresh indicator ("Last updated X seconds ago")
- [ ] **Commit:** `feat(frontend): upgrade anomaly UI with ML confidence`

#### Day 40 (Fri): Testing + Performance
- [ ] Comprehensive test pass: unit, integration, E2E
- [ ] Performance: query optimization, caching review, Docker image size
- [ ] Check BigQuery costs, optimize expensive queries
- [ ] **Commit:** `test: comprehensive test suite and performance optimization`

#### Day 41 (Sat): Final Documentation + Release
- [ ] Update architecture docs with M2 components
- [ ] New ADRs: Pub/Sub, Vertex AI
- [ ] Update README with new architecture diagram + screenshots
- [ ] Deploy final version
- [ ] Tag `v2.0.0`
- [ ] **Commit:** `docs: update documentation for v2.0 release`

#### Day 42 (Sun): Buffer + Stretch Goals
- [ ] Any remaining fixes
- [ ] Optional: Terraform IaC, notification bell, compare repos view
- [ ] **Final push**

**🎉 MILESTONE 2 COMPLETE — "DevScope Advanced"**
```
✅ Everything from Milestone 1, PLUS:
✅ GitHub webhooks with HMAC verification + idempotency
✅ Pub/Sub event streaming + dead-letter queue
✅ Apache Beam / Dataflow real-time pipeline
✅ Vertex AI anomaly detection with confidence scores
✅ ML vs rule-based anomaly comparison
✅ Chart anomaly overlays
✅ Dual-mode ingestion (real-time + batch fallback)
✅ Cloud Scheduler automation
✅ <30 second end-to-end event latency
```

---

## 8. PROJECT MANAGEMENT

### GitHub Project Board (Kanban)
```
Backlog → To Do → In Progress → In Review → Done
```

### Issue Labels
```
priority:critical    — Blocks other work
priority:high        — Must ship this phase
priority:medium      — Should ship this phase
priority:low         — Nice to have

type:feature         — New functionality
type:bug             — Something broken
type:chore           — Maintenance, refactor, config
type:docs            — Documentation
type:test            — Testing

component:backend    — Backend/API
component:frontend   — Dashboard
component:pipeline   — Data pipeline
component:ml         — ML / Vertex AI
component:infra      — Docker, CI/CD, GCP

milestone:core       — Milestone 1 (Weeks 1-4)
milestone:advanced   — Milestone 2 (Weeks 5-6)
```

### Branch Strategy
```
main                 — Production-ready, protected (CI must pass)
dev                  — Integration branch
feature/GH-{num}-*   — Feature branches
fix/GH-{num}-*       — Bug fixes
```

### Commit Convention
```
feat(backend): add PR latency metric computation
fix(frontend): correct date range filter timezone
chore(infra): update Dockerfile base image
docs: add BigQuery schema documentation
test(backend): add metrics service unit tests
```

### PR Template
```markdown
## What
<!-- Brief description -->

## Why
<!-- Motivation / linked issue -->

## How
<!-- Implementation approach -->

## Testing
<!-- How was this tested? -->

## Screenshots
<!-- If UI changes -->

## Checklist
- [ ] Tests added/updated
- [ ] Docs updated
- [ ] No console.log / print statements
- [ ] Types are accurate
- [ ] Pre-commit passes
```

### Daily Dev Log (`DEV_LOG.md`)
```markdown
## Day X — YYYY-MM-DD

### Goals
- [ ] Goal 1
- [ ] Goal 2

### Completed
- What I built, key decisions

### Blockers
- Issues and how I solved them

### Learnings
- New concepts / techniques

### Tomorrow
- Plan for next session
```

---

## 9. TECHNICAL CONCEPTS BY WEEK

| Week | Key Concepts |
|------|-------------|
| 1 | Docker Compose, SQLAlchemy async + Alembic, BigQuery SDK, httpx, circuit breaker, Celery, structlog, Sentry |
| 2 | OAuth2 authorization code flow, JWT (access + refresh), FastAPI dependency injection, cursor pagination, rate limiting, Redis caching, React Router + lazy loading, React Query |
| 3 | BigQuery analytical SQL (window functions, APPROX_QUANTILES), Recharts, SVG gauges, z-score anomaly detection, React Query polling |
| 4 | Docker multi-stage builds, Cloud Run + Cloud SQL + Memorystore, GitHub Actions CI/CD, Tailwind dark mode, accessibility (ARIA, keyboard nav), technical writing |
| 5 | Pub/Sub (topics, subscriptions, ack/nack), webhook HMAC, Apache Beam (PCollections, windowing, triggers), Dataflow deployment |
| 6 | Time-series feature engineering, Isolation Forest, Vertex AI (training, endpoints), Cloud Scheduler |

---

## 10. ENVIRONMENT VARIABLES (.env.example)

```env
# ─── Environment ───────────────────────────────────
ENVIRONMENT=development                   # development | test | production

# ─── PostgreSQL ────────────────────────────────────
DATABASE_URL=postgresql+asyncpg://devscope:devscope_local@localhost:5432/devscope_dev
DATABASE_URL_TEST=postgresql+asyncpg://devscope:devscope_local@localhost:5432/devscope_test

# ─── Redis ─────────────────────────────────────────
REDIS_URL=redis://localhost:6379/0

# ─── GitHub OAuth ──────────────────────────────────
GITHUB_CLIENT_ID=your-oauth-client-id
GITHUB_CLIENT_SECRET=your-oauth-client-secret
GITHUB_TOKEN=ghp_xxxxxxxxxxxx              # Personal access token (dev only)
GITHUB_WEBHOOK_SECRET=your-webhook-secret   # (M2)

# ─── JWT ───────────────────────────────────────────
JWT_SECRET_KEY=your-random-secret-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=15
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# ─── GCP ───────────────────────────────────────────
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# ─── BigQuery ──────────────────────────────────────
BQ_DATASET=devscope_dev                    # devscope_dev | devscope_prod
BQ_LOCATION=US

# ─── Pub/Sub (M2) ─────────────────────────────────
PUBSUB_TOPIC_EVENTS=github-events
PUBSUB_TOPIC_DLQ=github-events-dlq
PUBSUB_SUBSCRIPTION=github-events-sub

# ─── Vertex AI (M2) ───────────────────────────────
VERTEX_ENDPOINT_ID=your-endpoint-id
VERTEX_MODEL_ID=your-model-id

# ─── Sentry ────────────────────────────────────────
SENTRY_DSN=https://examplekey@sentry.io/1234567

# ─── App ───────────────────────────────────────────
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
LOG_LEVEL=INFO
```

---

## 11. MAKEFILE

```makefile
.PHONY: dev test lint format setup seed migrate

# ─── Setup ─────────────────────────────────────────
setup:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm ci
	pre-commit install

# ─── Infrastructure ────────────────────────────────
infra-up:
	docker compose -f infra/docker-compose.yml up -d

infra-down:
	docker compose -f infra/docker-compose.yml down

# ─── Database ──────────────────────────────────────
migrate:
	cd backend && alembic upgrade head

migrate-create:
	cd backend && alembic revision --autogenerate -m "$(msg)"

# ─── Development ───────────────────────────────────
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-worker:
	cd backend && celery -A workers.celery_app worker --loglevel=info

dev-frontend:
	cd frontend && npm run dev

dev:
	make -j3 dev-backend dev-worker dev-frontend

# ─── Testing ───────────────────────────────────────
test-backend:
	cd backend && pytest -v --cov=app --cov-report=term-missing --cov-fail-under=70

test-frontend:
	cd frontend && npm run test

test:
	make test-backend && make test-frontend

# ─── Quality ───────────────────────────────────────
lint:
	cd backend && ruff check app/ workers/
	cd frontend && npm run lint

format:
	cd backend && ruff format app/ workers/
	cd frontend && npx prettier --write src/

type-check:
	cd frontend && npx tsc --noEmit

precommit:
	pre-commit run --all-files

# ─── Data ──────────────────────────────────────────
seed:
	cd backend && python scripts/seed_data.py

# ─── Docker ────────────────────────────────────────
build:
	docker build -t devscope-backend ./backend
	docker build -t devscope-worker -f ./backend/Dockerfile.worker ./backend

# ─── Deploy ────────────────────────────────────────
deploy:
	gcloud builds submit --tag us-central1-docker.pkg.dev/$(GCP_PROJECT_ID)/devscope/backend:latest ./backend
	gcloud run deploy devscope --image=us-central1-docker.pkg.dev/$(GCP_PROJECT_ID)/devscope/backend:latest --region=us-central1

# ─── Deps ──────────────────────────────────────────
lock-deps:
	cd backend && pip-compile requirements.in -o requirements.txt
	cd backend && pip-compile requirements-dev.in -o requirements-dev.txt
```

---

## 12. COST ESTIMATES (GCP)

| Service | Free Tier | DevScope Usage | Monthly Cost |
|---------|-----------|---------------|--------------|
| BigQuery | 1TB queries, 10GB storage | ~5-20GB queries, <1GB storage | $0 |
| Cloud Run | 2M requests, 360K vCPU-sec | ~1K req/day | $0 |
| Cloud SQL (Postgres) | None | Smallest instance | **~$7-10** |
| Memorystore (Redis) | None | Basic 1GB | **~$10-15** |
| Pub/Sub (M2) | 10GB/month | <1GB | $0 |
| Dataflow (M2) | None | ~$1-5/hr when running | **$5-20** |
| Vertex AI (M2) | $300 free credit | Training + endpoint | **$10-30** |
| Artifact Registry | 500MB free | ~200MB | $0 |
| Secret Manager | 6 active versions free | ~10 secrets | $0 |

**Milestone 1 total: ~$17-25/month** (Cloud SQL + Memorystore)
**Milestone 2 additional: ~$15-50** (Dataflow + Vertex AI, only when testing)
**$300 free trial covers 10+ months of Milestone 1**

**Cost-saving tips:**
- Stop Cloud SQL when not working (or use smallest tier)
- For M2: stop Dataflow jobs and delete Vertex AI endpoints when not testing
- Use `DirectRunner` (local) for Beam development
- Set billing alerts at $50, $100, $200, $300

---

## 13. QUICK-START CHECKLIST (Before Day 1)

### Accounts
- [ ] GitHub account + Personal Access Token (`repo` + `read:org` scopes)
- [ ] GCP account with billing enabled ($300 free trial)
- [ ] Sentry account (free tier)

### GCP
- [ ] Create project
- [ ] Enable: BigQuery, Cloud Run, Artifact Registry, Cloud SQL Admin, Secret Manager
- [ ] Create service account (BigQuery Admin, Cloud Run Admin, Secret Manager Accessor, Cloud SQL Client)
- [ ] Download JSON key
- [ ] `gcloud auth login && gcloud config set project YOUR_PROJECT`
- [ ] Set billing alerts

### Local Tools
- [ ] Python 3.11+
- [ ] Node.js 20+
- [ ] Docker Desktop
- [ ] Git with SSH key
- [ ] VS Code + extensions: Python, ESLint, Tailwind IntelliSense, Prettier, GitLens

### Bookmarks
- [ ] [GitHub REST API](https://docs.github.com/en/rest)
- [ ] [FastAPI](https://fastapi.tiangolo.com)
- [ ] [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [ ] [Alembic](https://alembic.sqlalchemy.org/)
- [ ] [BigQuery SQL](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [ ] [Recharts](https://recharts.org)
- [ ] [React Query](https://tanstack.com/query/latest)
- [ ] [Tailwind CSS](https://tailwindcss.com/docs)
- [ ] [Apache Beam Python](https://beam.apache.org/documentation/sdks/python/) (Week 5)
- [ ] [Vertex AI](https://cloud.google.com/vertex-ai/docs) (Week 6)
