# DevScope — Repository Intelligence Tool
## Complete Project Plan & Build Guide (v2)

---

## 1. PROJECT OVERVIEW

**What DevScope Does:**
A distributed engineering productivity platform that mines GitHub repositories via the GitHub API, correlates developer metrics (PR latency, code churn, review cycles), streams events through Google Cloud Pub/Sub into BigQuery for sub-second querying, and uses Vertex AI for time-series anomaly detection — all surfaced through a React/TypeScript dashboard.

**Tech Stack:**
- **Frontend:** React 18 + TypeScript, Vite, TailwindCSS, Recharts/D3.js
- **Backend:** Python (FastAPI), GitHub REST/GraphQL API
- **Cloud:** GCP — BigQuery, Vertex AI, Cloud Run, Pub/Sub, Cloud Dataflow
- **Infrastructure:** Docker, GitHub Actions CI/CD
- **Testing:** Pytest, React Testing Library, Vitest

---

## 2. MILESTONE STRATEGY

This project is built in two milestones so you always have a working, demo-ready product.

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MILESTONE 1 — "DevScope Core" (Weeks 1–3)                            │
│  Demo-ready. Resume-valid. Fully functional without cloud complexity.  │
│                                                                        │
│  GitHub API ──► Batch Ingestion ──► BigQuery ──► FastAPI ──► React     │
│                   (cron/manual)                   + z-score anomalies  │
│                                                                        │
│  Week 1: Foundation (GCP + GitHub client + BigQuery + project setup)   │
│  Week 2: Metrics Engine (computation + API + chart dashboard)          │
│  Week 3: Frontend Polish + Basic Anomalies + Deploy v1                 │
├─────────────────────────────────────────────────────────────────────────┤
│  MILESTONE 2 — "DevScope Advanced" (Weeks 4–5)                        │
│  Cloud-native upgrade on top of a working system.                      │
│                                                                        │
│  GitHub Webhooks ──► Pub/Sub ──► Dataflow ──► BigQuery                │
│                                   Vertex AI anomaly detection          │
│                                                                        │
│  Week 4: Real-Time Pipeline (Pub/Sub + Webhooks + Dataflow)           │
│  Week 5: ML Anomaly Detection (Vertex AI) + Final Polish              │
└─────────────────────────────────────────────────────────────────────────┘
```

**Why this structure works:**
- After Week 3 you have a complete, deployable project — if interviews come up or SNHU gets busy, you're covered
- Milestone 2 enhances a working system instead of building 5 complex systems from scratch simultaneously
- Each week has a clear deliverable you can commit, push, and point to
- You learn incrementally: APIs → data → visualization → streaming → ML

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
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md
│       ├── feature_request.md
│       └── task.md
│
├── docs/
│   ├── architecture.md               # System architecture diagram + decisions
│   ├── api-reference.md              # API endpoint documentation
│   ├── data-model.md                 # BigQuery schemas, entity relationships
│   ├── setup-guide.md                # Local dev + GCP setup instructions
│   ├── deployment.md                 # Cloud Run deployment runbook
│   └── adr/                          # Architecture Decision Records
│       ├── 001-use-pubsub-over-kafka.md
│       ├── 002-bigquery-over-postgres.md
│       └── 003-vertex-ai-anomaly-detection.md
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── config.py                 # Environment config (pydantic-settings)
│   │   ├── dependencies.py           # Dependency injection
│   │   │
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── router.py             # Top-level router aggregation
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── repos.py          # /api/v1/repos — repo onboarding
│   │   │   │   ├── metrics.py        # /api/v1/metrics — query metrics
│   │   │   │   ├── anomalies.py      # /api/v1/anomalies — anomaly results
│   │   │   │   ├── health.py         # /api/v1/health — healthcheck
│   │   │   │   └── webhooks.py       # /api/v1/webhooks — GitHub webhook receiver (M2)
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── github_client.py      # GitHub API wrapper (REST + GraphQL)
│   │   │   ├── pubsub_publisher.py   # Pub/Sub message publishing (M2)
│   │   │   ├── bigquery_client.py    # BigQuery read/write operations
│   │   │   └── vertex_client.py      # Vertex AI inference client (M2)
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── repo_service.py       # Business logic: repo onboarding
│   │   │   ├── metrics_service.py    # Business logic: metric computation
│   │   │   ├── ingestion_service.py  # Business logic: event ingestion
│   │   │   └── anomaly_service.py    # Business logic: anomaly detection
│   │   │
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── schemas.py            # Pydantic request/response schemas
│   │   │   └── enums.py              # Shared enums
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── rate_limiter.py       # GitHub API rate limit handling
│   │       └── logger.py             # Structured logging setup
│   │
│   ├── workers/
│   │   ├── __init__.py
│   │   ├── event_processor.py        # Pub/Sub subscriber (M2)
│   │   └── batch_ingester.py         # Historical data backfill worker
│   │
│   ├── dataflow/
│   │   ├── pipeline.py               # Apache Beam pipeline definition (M2)
│   │   └── transforms.py             # Custom PTransforms (M2)
│   │
│   ├── ml/
│   │   ├── train.py                  # Vertex AI training job script (M2)
│   │   ├── predict.py                # Batch/online prediction (M2)
│   │   └── preprocessing.py          # Feature engineering for time series (M2)
│   │
│   ├── tests/
│   │   ├── conftest.py               # Shared fixtures
│   │   ├── unit/
│   │   │   ├── test_github_client.py
│   │   │   ├── test_metrics_service.py
│   │   │   └── test_anomaly_service.py
│   │   ├── integration/
│   │   │   ├── test_bigquery.py
│   │   │   └── test_pubsub.py
│   │   └── e2e/
│   │       └── test_full_pipeline.py
│   │
│   ├── scripts/
│   │   ├── seed_data.py              # Seed BigQuery with sample data
│   │   ├── setup_gcp.sh              # One-click GCP resource provisioning
│   │   └── run_backfill.py           # Historical data ingestion
│   │
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   └── pyproject.toml
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx                  # App entry
│   │   ├── App.tsx                   # Root component + routing
│   │   ├── vite-env.d.ts
│   │   │
│   │   ├── api/
│   │   │   ├── client.ts             # Axios/fetch wrapper with interceptors
│   │   │   ├── repos.ts              # Repo API calls
│   │   │   ├── metrics.ts            # Metrics API calls
│   │   │   └── anomalies.ts          # Anomaly API calls
│   │   │
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── DashboardLayout.tsx
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
│   │   │       └── DateRangePicker.tsx
│   │   │
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx          # Main overview page
│   │   │   ├── RepoDetail.tsx         # Single repo deep-dive
│   │   │   ├── Anomalies.tsx          # Anomaly feed
│   │   │   ├── Settings.tsx           # User/org settings
│   │   │   └── Onboarding.tsx         # Connect GitHub + add repos
│   │   │
│   │   ├── hooks/
│   │   │   ├── useMetrics.ts          # React Query hook for metrics
│   │   │   ├── useRepos.ts            # React Query hook for repos
│   │   │   └── useAnomalies.ts        # React Query hook for anomalies
│   │   │
│   │   ├── store/
│   │   │   └── index.ts              # Zustand or React Context store
│   │   │
│   │   ├── types/
│   │   │   ├── metrics.ts            # TypeScript interfaces for metrics
│   │   │   ├── repos.ts
│   │   │   └── anomalies.ts
│   │   │
│   │   └── utils/
│   │       ├── formatters.ts          # Number/date formatting
│   │       └── constants.ts           # App-wide constants
│   │
│   ├── public/
│   │   └── favicon.svg
│   ├── index.html
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── package.json
│   └── .eslintrc.cjs
│
├── infra/
│   ├── terraform/                    # (Optional) IaC for GCP resources
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── docker-compose.yml            # Local dev environment
│
├── .gitignore
├── .env.example                      # Template for env vars
├── README.md                         # Project overview + quick start
├── CONTRIBUTING.md                   # How to contribute
├── LICENSE
├── Makefile                          # Common commands (make dev, make test, etc.)
├── DEV_LOG.md                        # Daily progress journal
└── CHANGELOG.md                      # Version history
```

**(M2)** = Added in Milestone 2. Create the file/folder during setup but leave it empty with a `# TODO: Milestone 2` comment so the structure is ready.

---

## 4. COMPLETE FEATURE LIST

### 4.1 — GitHub Integration
- [ ] GitHub OAuth2 app registration + token management
- [ ] REST API client with automatic rate-limit handling (retry + backoff)
- [ ] GraphQL client for batch queries (PRs, reviews, commits)
- [ ] Repository onboarding flow (connect → validate → start ingestion)
- [ ] Support for org-level and individual repo connections
- [ ] Historical data backfill (paginate through past PRs/commits)
- [ ] **(M2)** Webhook receiver for real-time push events (PR opened, merged, review submitted)

### 4.2 — Data Ingestion & Streaming
- [ ] Batch ingestion service (manual trigger + cron-based refresh)
- [ ] Idempotent ingestion (skip already-processed events by ID)
- [ ] **(M2)** Pub/Sub topic creation and message publishing
- [ ] **(M2)** Message schema definition (Avro or JSON schema)
- [ ] **(M2)** Event types: PR_OPENED, PR_MERGED, PR_CLOSED, REVIEW_SUBMITTED, COMMIT_PUSHED
- [ ] **(M2)** Dead-letter topic for failed messages
- [ ] **(M2)** Pub/Sub subscriber worker for event processing

### 4.3 — Data Storage (BigQuery)
- [ ] Schema design for tables: `raw_events`, `pull_requests`, `commits`, `reviews`, `daily_metrics`, `anomalies`
- [ ] Partitioned tables (by date) for query performance
- [ ] Clustered tables (by repo_id) for efficient filtering
- [ ] Materialized views for pre-aggregated metrics
- [ ] Data retention policies (raw events: 90 days, aggregated: unlimited)
- [ ] Seed script with realistic sample data

### 4.4 — Metric Computation
- [ ] **PR Latency** — time from PR open to first review, to approval, to merge
- [ ] **Code Churn** — lines added vs deleted per PR, rework ratio
- [ ] **Review Cycles** — number of review rounds per PR, review turnaround time
- [ ] **Deployment Frequency** — merges to main per day/week
- [ ] **Throughput** — PRs merged per developer per week
- [ ] **Health Score** — composite 0-100 score from weighted sub-metrics
- [ ] Time-windowed aggregations (daily, weekly, monthly)
- [ ] Per-developer and per-repo metric breakdowns

### 4.5 — Anomaly Detection
- [ ] **M1: Statistical anomalies** — z-score thresholds on metric time series (flag values >2σ from rolling mean)
- [ ] **M1: Simple alert rules** — PR latency > X hours, churn spike > Y%, review rounds > Z
- [ ] **(M2)** Feature engineering for time-series data (lag features, rolling stats)
- [ ] **(M2)** Vertex AI model training (AutoML or custom IsolationForest)
- [ ] **(M2)** Online prediction endpoint deployment
- [ ] **(M2)** Confidence scores for each detected anomaly
- [ ] **(M2)** Scheduled retraining job (weekly)

### 4.6 — Stream Processing (Cloud Dataflow) — M2 Only
- [ ] **(M2)** Apache Beam pipeline for real-time metric aggregation
- [ ] **(M2)** Sliding window computations (1h, 24h, 7d rolling metrics)
- [ ] **(M2)** Tumbling window for daily snapshots
- [ ] **(M2)** Side inputs for repo metadata enrichment
- [ ] **(M2)** Pipeline monitoring and autoscaling

### 4.7 — Backend API (FastAPI)
- [ ] `POST /api/v1/repos` — onboard new repository
- [ ] `GET /api/v1/repos` — list connected repos
- [ ] `GET /api/v1/repos/{id}` — repo detail
- [ ] `DELETE /api/v1/repos/{id}` — disconnect repo
- [ ] `GET /api/v1/metrics?repo_id=&window=&group_by=` — query metrics
- [ ] `GET /api/v1/metrics/{repo_id}/health` — health score
- [ ] `GET /api/v1/anomalies?repo_id=&severity=` — anomaly feed
- [ ] `GET /api/v1/health` — service healthcheck
- [ ] **(M2)** `POST /api/v1/webhooks/github` — webhook receiver
- [ ] API key authentication middleware
- [ ] Request validation, error handling, structured logging
- [ ] OpenAPI/Swagger documentation auto-generation
- [ ] CORS configuration

### 4.8 — Frontend Dashboard (React/TypeScript)
- [ ] **Onboarding page** — input repo owner/name → trigger ingestion
- [ ] **Dashboard overview** — summary cards (total repos, avg health score, active anomalies)
- [ ] **PR Latency chart** — line/area chart with time range selector
- [ ] **Code Churn chart** — stacked bar (additions vs deletions)
- [ ] **Review Cycles chart** — distribution histogram
- [ ] **Anomaly timeline** — flagged events with severity color coding
- [ ] **Health Score gauge** — per-repo radial gauge (0-100)
- [ ] **Repo detail page** — deep dive with all metrics for one repo
- [ ] **Date range picker** — filter all charts by custom window
- [ ] **Developer breakdown** — contributor-level metric table
- [ ] **Settings page** — notification preferences, repo management
- [ ] Responsive layout (desktop-first, tablet-friendly)
- [ ] Dark/light mode toggle
- [ ] Loading states, error boundaries, empty states
- [ ] React Query for server state management + caching

### 4.9 — Deployment & DevOps
- [ ] Backend Dockerfile (multi-stage build)
- [ ] Cloud Run service deployment (backend)
- [ ] Frontend build → served via Cloud Run or Cloud Storage + CDN
- [ ] GitHub Actions CI pipeline (lint, test, type-check)
- [ ] GitHub Actions CD pipeline (build, push image, deploy)
- [ ] Environment variable management (.env.example)
- [ ] Makefile for common commands
- [ ] Health check endpoint for Cloud Run

---

## 5. WEEK-BY-WEEK BUILD PLAN

---

### ═══════════════════════════════════════════════════
### MILESTONE 1 — "DevScope Core" (Weeks 1–3)
### ═══════════════════════════════════════════════════

**End state:** A fully working app where you can onboard a GitHub repo, see real metrics on a polished dashboard, get basic anomaly alerts, and deploy to Cloud Run. This alone matches your resume bullet points.

---

### WEEK 1 — FOUNDATION
**Goal:** GCP configured, GitHub data flowing into BigQuery, basic API serving data, React app rendering.

**Deliverable by end of week:** You can run a script that pulls PR/commit data from any public GitHub repo, stores it in BigQuery, and query it through a FastAPI endpoint that a bare-bones React app calls.

---

#### Day 1 (Mon): Project Scaffolding + GCP Setup
**Focus: Get the boring-but-critical stuff out of the way.**

**Morning — Project Init (2–3 hours)**
- [ ] Create GitHub repo: `devscope`
- [ ] Set up the full directory structure (copy from Section 3 above)
- [ ] Initialize backend:
  - `pyproject.toml` with project metadata
  - `requirements.txt`: fastapi, uvicorn, httpx, google-cloud-bigquery, pydantic-settings, python-dotenv
  - `requirements-dev.txt`: pytest, pytest-asyncio, ruff, mypy
  - Virtual environment: `python -m venv venv`
- [ ] Initialize frontend:
  - `npm create vite@latest frontend -- --template react-ts`
  - Install: `npm i tailwindcss @tailwindcss/vite react-router-dom @tanstack/react-query recharts axios`
  - Configure Tailwind with Vite plugin
- [ ] Create `.env.example` with all variables (see Section 9)
- [ ] Create `Makefile` with `dev`, `test`, `lint` targets
- [ ] Create `.gitignore` (Python + Node + GCP)
- [ ] Write initial `README.md`
- [ ] **Commit:** `chore: initialize project structure with backend and frontend scaffolding`

**Afternoon — GCP Setup (2–3 hours)**
- [ ] Create GCP project (or use existing one)
- [ ] Enable APIs: BigQuery, Cloud Run, Artifact Registry
  - *Note: Skip Pub/Sub, Dataflow, Vertex AI for now — that's Milestone 2*
- [ ] Create service account with roles: BigQuery Admin, Cloud Run Admin
- [ ] Download service account JSON key → add path to `.env`
- [ ] Install `gcloud` CLI, authenticate: `gcloud auth login`
- [ ] Set project: `gcloud config set project YOUR_PROJECT_ID`
- [ ] Test connection: run a simple BigQuery query from Python
- [ ] **Commit:** `chore(infra): configure GCP project and service account`

**Evening — Verify Everything Runs**
- [ ] `make dev-backend` starts FastAPI with "Hello DevScope" at `/api/v1/health`
- [ ] `make dev-frontend` starts React app with "DevScope" heading
- [ ] Both run without errors
- [ ] **Commit:** `feat: add health endpoint and frontend shell`

**🧠 Learning Focus:** GCP Console navigation, IAM roles, service accounts, gcloud CLI, Vite + Tailwind setup

**⚠️ Common Blockers:**
- GCP billing setup — need a credit card even for free tier
- Service account permissions — if BigQuery queries fail with 403, check IAM roles
- Python virtual environment confusion — always activate with `source venv/bin/activate`

---

#### Day 2 (Tue): GitHub API Client
**Focus: Build a robust, well-tested GitHub API wrapper.**

**Morning — Core Client (3 hours)**
- [ ] Register a GitHub Personal Access Token (classic, `repo` + `read:org` scopes)
- [ ] Build `backend/app/core/github_client.py`:
  ```python
  class GitHubClient:
      async def get_repo(owner, name) -> RepoInfo
      async def list_pull_requests(owner, name, state, per_page, page) -> list[PR]
      async def get_pull_request(owner, name, number) -> PRDetail
      async def list_commits(owner, name, since, until) -> list[Commit]
      async def list_reviews(owner, name, pr_number) -> list[Review]
  ```
- [ ] Use `httpx.AsyncClient` with:
  - Base URL: `https://api.github.com`
  - Auth header: `Authorization: Bearer {token}`
  - Accept header: `application/vnd.github.v3+json`
- [ ] Parse `Link` header for pagination (GitHub uses RFC 5988 link relations)
- [ ] Build a `paginate_all()` helper that follows `next` links

**Afternoon — Rate Limiting + Error Handling (2 hours)**
- [ ] Read `X-RateLimit-Remaining` and `X-RateLimit-Reset` from response headers
- [ ] Implement pre-request check: if remaining < 10, sleep until reset time
- [ ] Add exponential backoff for 5xx errors (retry 3 times with 1s, 2s, 4s delays)
- [ ] Handle 404 (repo not found), 401 (bad token), 403 (rate limited) with custom exceptions
- [ ] Add structured logging: log every API call with method, URL, status, rate limit remaining

**Evening — Testing (1–2 hours)**
- [ ] Write unit tests for `github_client.py` using `httpx` mock transport
- [ ] Test: successful fetch, pagination, rate limit detection, error handling
- [ ] Test with a real public repo: `fetch facebook/react PRs` — verify data shape
- [ ] **Commit:** `feat(backend): add GitHub API client with rate limiting and pagination`

**🧠 Learning Focus:** httpx async client, GitHub API pagination, rate limiting patterns, pytest-asyncio

**⚠️ Common Blockers:**
- GitHub API returns nested data — print raw responses first to understand the shape
- Pagination: the `Link` header format is tricky to parse, use a regex or library
- Rate limits: 5,000 req/hour for authenticated requests — plenty for dev, but log it

---

#### Day 3 (Wed): BigQuery Schemas + Client
**Focus: Design your data model and build reliable BigQuery operations.**

**Morning — Schema Design (2–3 hours)**
- [ ] Create BigQuery dataset: `devscope`
- [ ] Design and create tables with SQL DDL (or Python SDK):

  **`repositories`** — onboarded repos
  ```
  repo_id STRING (PK), owner STRING, name STRING, full_name STRING,
  default_branch STRING, language STRING, stars INT64, forks INT64,
  onboarded_at TIMESTAMP, last_synced_at TIMESTAMP
  ```

  **`pull_requests`** — enriched PR records (PARTITIONED BY created_date)
  ```
  pr_id STRING (PK), repo_id STRING, number INT64, title STRING,
  author STRING, state STRING, created_at TIMESTAMP, first_review_at TIMESTAMP,
  approved_at TIMESTAMP, merged_at TIMESTAMP, closed_at TIMESTAMP,
  additions INT64, deletions INT64, changed_files INT64, review_rounds INT64,
  created_date DATE (partition column)
  ```

  **`commits`** — commit records (PARTITIONED BY committed_date)
  ```
  commit_sha STRING (PK), repo_id STRING, author STRING, message STRING,
  committed_at TIMESTAMP, additions INT64, deletions INT64,
  committed_date DATE (partition column)
  ```

  **`reviews`** — PR review records
  ```
  review_id STRING (PK), pr_id STRING, repo_id STRING, reviewer STRING,
  state STRING (APPROVED/CHANGES_REQUESTED/COMMENTED),
  submitted_at TIMESTAMP
  ```

  **`daily_metrics`** — pre-aggregated stats (PARTITIONED BY metric_date)
  ```
  repo_id STRING, metric_date DATE, metric_name STRING, metric_value FLOAT64,
  developer STRING (nullable — NULL means repo-level aggregate)
  ```

  **`anomalies`** — detected anomalies
  ```
  anomaly_id STRING (PK), repo_id STRING, detected_at TIMESTAMP,
  anomaly_type STRING, metric_name STRING, expected_value FLOAT64,
  actual_value FLOAT64, severity STRING (LOW/MEDIUM/HIGH/CRITICAL),
  confidence FLOAT64, resolved BOOL
  ```

- [ ] Add clustering on `repo_id` for all tables

**Afternoon — BigQuery Client (2–3 hours)**
- [ ] Build `backend/app/core/bigquery_client.py`:
  ```python
  class BigQueryClient:
      async def insert_rows(table, rows) -> None        # Streaming insert
      async def query(sql, params) -> list[dict]         # Parameterized query
      async def create_table_if_not_exists(schema) -> None
      async def get_repo(repo_id) -> dict | None
      async def list_repos() -> list[dict]
  ```
- [ ] Use parameterized queries everywhere (never string-format SQL)
- [ ] Handle BigQuery errors: table not found, quota exceeded, invalid schema
- [ ] Test: insert a row, query it back, verify types

**Evening — Integration Test**
- [ ] Write integration test: create table → insert → query → delete
- [ ] **Commit:** `feat(backend): add BigQuery schemas and client with CRUD operations`

**🧠 Learning Focus:** BigQuery table design (partitioning, clustering, why they matter), Google Cloud Python SDK, parameterized queries

**⚠️ Common Blockers:**
- BigQuery streaming inserts have a delay (~seconds) — don't query immediately after insert in tests
- Partition columns must be DATE or TIMESTAMP, not STRING
- BigQuery is case-sensitive for dataset/table names

---

#### Day 4 (Thu): Ingestion Service
**Focus: Pull data from GitHub, transform it, load it into BigQuery.**

**Morning — Ingestion Logic (3 hours)**
- [ ] Build `backend/app/services/ingestion_service.py`:
  ```python
  class IngestionService:
      async def onboard_repo(owner, name) -> RepoInfo
          # 1. Fetch repo metadata from GitHub
          # 2. Insert into repositories table
          # 3. Kick off historical backfill

      async def backfill_repo(repo_id, owner, name) -> BackfillResult
          # 1. Paginate through ALL PRs (closed + open)
          # 2. For each PR: fetch reviews
          # 3. Paginate through commits (last 90 days)
          # 4. Transform all data → BigQuery row format
          # 5. Batch insert into BigQuery

      async def sync_repo(repo_id, owner, name, since) -> SyncResult
          # Incremental: only fetch PRs/commits since last_synced_at
  ```
- [ ] Build transformer functions: GitHub API response → BigQuery row
  - Extract `first_review_at` from reviews list (earliest review timestamp)
  - Calculate `review_rounds` (count unique review submissions)
  - Map PR state correctly (open, closed, merged)

**Afternoon — Batch Insert + Error Handling (2 hours)**
- [ ] Implement batch inserts (BigQuery streaming insert limit: 500 rows/request)
- [ ] Add progress logging: "Ingesting PRs: 150/342 complete"
- [ ] Handle partial failures (some rows fail, others succeed)
- [ ] Add idempotency: check if PR/commit already exists before inserting (by ID)

**Evening — Test with Real Data (1–2 hours)**
- [ ] Run ingestion against a real repo (start small: your own repo or a small open source one)
- [ ] Then try a medium repo (e.g., `pallets/flask` — ~5K PRs)
- [ ] Verify data in BigQuery Console — spot check 5-10 PRs manually
- [ ] **Commit:** `feat(backend): add ingestion service with historical backfill`

**🧠 Learning Focus:** ETL patterns, data transformation, batch processing, idempotent operations

**⚠️ Common Blockers:**
- GitHub pagination can be slow for large repos — add logging so you know it's working
- Datetime parsing: GitHub returns ISO 8601 strings, BigQuery wants TIMESTAMP — use `fromisoformat()`
- Some PRs have no reviews — handle None/empty gracefully

---

#### Day 5 (Fri): FastAPI Endpoints
**Focus: Build the API layer that the frontend will consume.**

**Morning — Core Endpoints (3 hours)**
- [ ] Build `backend/app/main.py`:
  - FastAPI app with lifespan (initialize clients on startup, cleanup on shutdown)
  - CORS middleware (allow frontend origin)
  - Global exception handler
- [ ] Build Pydantic schemas (`models/schemas.py`):
  ```python
  class RepoCreate(BaseModel): owner: str, name: str
  class RepoResponse(BaseModel): repo_id, full_name, stars, health_score, last_synced_at
  class MetricPoint(BaseModel): date: date, value: float
  class MetricResponse(BaseModel): metric: str, values: list[MetricPoint], summary: MetricSummary
  class AnomalyResponse(BaseModel): anomaly_id, type, severity, confidence, detected_at
  ```
- [ ] Implement endpoints:
  - `POST /api/v1/repos` — calls `ingestion_service.onboard_repo()`
  - `GET /api/v1/repos` — calls `bigquery_client.list_repos()`
  - `GET /api/v1/repos/{repo_id}` — repo detail with latest metrics
  - `DELETE /api/v1/repos/{repo_id}` — remove repo (soft delete)
  - `GET /api/v1/health` — return `{ status: "ok", version: "0.1.0" }`

**Afternoon — Dependency Injection + Config (2 hours)**
- [ ] Build `config.py` with pydantic-settings (loads from `.env`)
- [ ] Build `dependencies.py`:
  - `get_github_client()` → shared httpx client
  - `get_bigquery_client()` → shared BQ client
  - `get_ingestion_service()` → wired with above clients
- [ ] Use FastAPI `Depends()` throughout endpoints
- [ ] Verify Swagger UI at `http://localhost:8000/docs`
- [ ] Test each endpoint with curl or Swagger

**Evening — Tests + Polish**
- [ ] Write endpoint tests using FastAPI `TestClient`
- [ ] Test error cases: invalid repo, missing fields, non-existent repo_id
- [ ] **Commit:** `feat(backend): add REST API endpoints for repos with dependency injection`

**🧠 Learning Focus:** FastAPI dependency injection, Pydantic validation, OpenAPI auto-generation, async patterns

---

#### Day 6 (Sat): Frontend Shell + API Integration
**Focus: Get the React app talking to your backend.**

**Morning — Layout + Routing (3 hours)**
- [ ] Set up React Router:
  - `/` → Dashboard
  - `/repos/:repoId` → RepoDetail
  - `/anomalies` → Anomalies
  - `/settings` → Settings
- [ ] Build `DashboardLayout.tsx`:
  - Sidebar (left, collapsible) with nav links
  - Header bar (app name, placeholder user avatar)
  - Main content area
- [ ] Build `Sidebar.tsx` — links with active state highlighting (use `NavLink`)
- [ ] Style with Tailwind — clean, minimal, dark sidebar + light content area

**Afternoon — API Layer + Repo Onboarding (3 hours)**
- [ ] Build `frontend/src/api/client.ts`:
  - Axios instance with `baseURL: import.meta.env.VITE_API_URL`
  - Response interceptor for error handling
- [ ] Build `frontend/src/api/repos.ts`:
  - `fetchRepos()`, `fetchRepo(id)`, `createRepo(owner, name)`, `deleteRepo(id)`
- [ ] Build `useRepos.ts` hook with React Query:
  ```typescript
  export function useRepos() {
    return useQuery({ queryKey: ['repos'], queryFn: fetchRepos })
  }
  ```
- [ ] Build `Onboarding.tsx` — simple form: owner + repo name → POST /repos → redirect to dashboard
- [ ] Build `RepoCard.tsx` and `RepoList.tsx` — display onboarded repos on dashboard

**Evening — Verify End-to-End**
- [ ] Start backend + frontend
- [ ] Onboard a repo through the UI → see it appear in the repo list
- [ ] Verify data landed in BigQuery
- [ ] **Commit:** `feat(frontend): add dashboard layout, routing, and repo onboarding flow`

**🧠 Learning Focus:** React Router v6, React Query basics (queries, mutations, cache invalidation), Axios interceptors

---

#### Day 7 (Sun): Week 1 Review + Catch-Up
**Focus: Tie up loose ends, refactor, document.**

- [ ] Review all code — fix any TODO comments
- [ ] Refactor anything that feels messy (you'll know by now)
- [ ] Write `docs/setup-guide.md` — anyone should be able to clone and run your project
- [ ] Update `README.md` with "Quick Start" section
- [ ] Run full test suite, fix failures
- [ ] Manual end-to-end test: onboard 2-3 different repos
- [ ] Write `DEV_LOG.md` entry summarizing Week 1 learnings
- [ ] **Commit:** `docs: add setup guide and Week 1 dev log`
- [ ] **Push everything to GitHub**

**Week 1 Checkpoint:** You should now have:
```
✅ GCP project configured with BigQuery
✅ GitHub API client with pagination + rate limiting
✅ BigQuery schemas (6 tables) with working client
✅ Ingestion pipeline: GitHub → transform → BigQuery
✅ FastAPI with 5+ endpoints and Swagger docs
✅ React app with routing, layout, repo onboarding
✅ End-to-end: onboard repo via UI → data in BigQuery → visible in app
```

---

### WEEK 2 — METRICS ENGINE + DASHBOARD
**Goal:** Compute real engineering metrics from BigQuery data and display them on interactive charts.

**Deliverable by end of week:** Dashboard shows PR latency, code churn, review cycles, health scores, and developer breakdowns with interactive charts and date filtering.

---

#### Day 8 (Mon): Metric Computation — PR Latency & Throughput
**Focus: Write the SQL that powers your core metrics.**

**Morning — Metrics Service Setup (2 hours)**
- [ ] Build `backend/app/services/metrics_service.py` skeleton:
  ```python
  class MetricsService:
      async def get_pr_latency(repo_id, window) -> MetricResponse
      async def get_code_churn(repo_id, window) -> MetricResponse
      async def get_review_cycles(repo_id, window) -> MetricResponse
      async def get_throughput(repo_id, window) -> MetricResponse
      async def get_health_score(repo_id) -> HealthScore
      async def get_developer_metrics(repo_id, window) -> list[DeveloperMetrics]
  ```
- [ ] Build window helper: convert "7d", "30d", "90d" → date range

**Afternoon — PR Latency SQL (3 hours)**
- [ ] Write BigQuery SQL for PR latency:
  ```sql
  -- Time to first review (median + p95)
  SELECT
    DATE(created_at) as date,
    APPROX_QUANTILES(
      TIMESTAMP_DIFF(first_review_at, created_at, HOUR), 100
    )[OFFSET(50)] as median_hours,
    APPROX_QUANTILES(
      TIMESTAMP_DIFF(first_review_at, created_at, HOUR), 100
    )[OFFSET(95)] as p95_hours
  FROM pull_requests
  WHERE repo_id = @repo_id
    AND created_date BETWEEN @start_date AND @end_date
    AND first_review_at IS NOT NULL
  GROUP BY date
  ORDER BY date
  ```
- [ ] Write similar query for time-to-merge
- [ ] Implement `get_throughput()` — PRs merged per week
- [ ] Test each query in BigQuery Console first, then wire into service

**Evening — Metrics API Endpoint**
- [ ] Implement `GET /api/v1/metrics?repo_id=&metric=pr_latency&window=30d`
- [ ] Response format: `{ metric, values: [{date, value}], summary: {avg, p50, p95, trend} }`
- [ ] Test with curl against real ingested data
- [ ] **Commit:** `feat(backend): add PR latency and throughput metric computation`

**🧠 Learning Focus:** BigQuery analytical SQL (APPROX_QUANTILES, TIMESTAMP_DIFF, window functions), metric API design

---

#### Day 9 (Tue): Metric Computation — Churn, Reviews, Health Score
**Focus: Complete all metric computations and the composite health score.**

**Morning — Code Churn + Review Cycles (3 hours)**
- [ ] Code Churn SQL:
  ```sql
  SELECT DATE(created_at) as date,
    SUM(additions) as total_additions,
    SUM(deletions) as total_deletions,
    SUM(additions + deletions) as total_churn
  FROM pull_requests
  WHERE repo_id = @repo_id AND created_date BETWEEN @start_date AND @end_date
  GROUP BY date ORDER BY date
  ```
- [ ] Review Cycles SQL:
  ```sql
  SELECT review_rounds, COUNT(*) as pr_count
  FROM pull_requests
  WHERE repo_id = @repo_id AND created_date BETWEEN @start_date AND @end_date
  GROUP BY review_rounds ORDER BY review_rounds
  ```
- [ ] Review turnaround time: avg time between review rounds

**Afternoon — Health Score + Developer Breakdown (3 hours)**
- [ ] Design health score formula (weighted composite, 0-100):
  ```
  health_score = (
    0.30 × normalize(median_pr_latency, lower_is_better) +
    0.25 × normalize(review_turnaround, lower_is_better) +
    0.20 × normalize(throughput, higher_is_better) +
    0.15 × normalize(avg_review_rounds, lower_is_better) +
    0.10 × normalize(churn_ratio, lower_is_better)
  ) × 100
  ```
- [ ] Implement `get_health_score()` — run sub-queries, normalize, combine
- [ ] Implement `get_developer_metrics()` — same queries grouped by `author`
- [ ] Wire up remaining API endpoints

**Evening — Test All Metrics**
- [ ] Test each metric endpoint with real repo data
- [ ] Verify health score range makes sense (compare repos you know)
- [ ] **Commit:** `feat(backend): add code churn, review cycles, health score, and developer metrics`

**🧠 Learning Focus:** Composite scoring systems, data normalization, per-group aggregation

---

#### Day 10 (Wed): Dashboard Charts — PR Latency + Code Churn
**Focus: Build your first interactive charts with real data.**

**Morning — Chart Infrastructure (2 hours)**
- [ ] Build `frontend/src/api/metrics.ts`:
  - `fetchMetric(repoId, metric, window)`
  - `fetchHealthScore(repoId)`
  - `fetchDeveloperMetrics(repoId, window)`
- [ ] Build `useMetrics.ts` hook:
  ```typescript
  export function useMetric(repoId: string, metric: string, window: string) {
    return useQuery({
      queryKey: ['metrics', repoId, metric, window],
      queryFn: () => fetchMetric(repoId, metric, window),
      staleTime: 5 * 60 * 1000, // 5 min cache
    })
  }
  ```
- [ ] Build `MetricCard.tsx` — number + label + trend arrow (↑↓)

**Afternoon — PR Latency + Code Churn Charts (3 hours)**
- [ ] Build `PRLatencyChart.tsx`:
  - Recharts `AreaChart` with two lines: median (solid) and p95 (dashed)
  - X-axis: dates, Y-axis: hours
  - Tooltip showing exact values on hover
  - Responsive container
- [ ] Build `CodeChurnChart.tsx`:
  - Recharts `BarChart` with stacked bars: additions (green) and deletions (red)
  - X-axis: dates, Y-axis: lines of code
- [ ] Wire both charts to live API data through `useMetric` hook

**Evening — Polish**
- [ ] Add loading skeleton states for charts
- [ ] Add "No data" empty state
- [ ] Test with different window sizes (7d, 30d, 90d)
- [ ] **Commit:** `feat(frontend): add PR latency and code churn charts with live data`

**🧠 Learning Focus:** Recharts API (AreaChart, BarChart, Tooltip, ResponsiveContainer), React Query cache management

---

#### Day 11 (Thu): Dashboard Charts — Reviews, Health Gauge, Date Picker
**Focus: Complete the chart suite and add global filtering.**

**Morning — Remaining Charts (3 hours)**
- [ ] Build `ReviewCycleChart.tsx`:
  - Recharts `BarChart` showing distribution (x: review rounds, y: PR count)
  - Color gradient from green (1 round) to red (5+ rounds)
- [ ] Build `HealthScoreGauge.tsx`:
  - SVG radial gauge (0-100)
  - Color: green (80-100), yellow (50-79), red (0-49)
  - Animated fill on load
- [ ] Build `ThroughputChart.tsx`:
  - Simple line chart: PRs merged per week

**Afternoon — Date Picker + Dashboard Assembly (3 hours)**
- [ ] Build `DateRangePicker.tsx`:
  - Preset buttons: 7d, 30d, 90d, Custom
  - Custom range: two date inputs
  - Store selected range in URL params (so it persists on refresh)
- [ ] Build `Dashboard.tsx` page:
  - Top row: 4 `MetricCard` components (total PRs, avg latency, health score, active anomalies)
  - `DateRangePicker` below cards
  - 2×2 grid of charts: PR Latency | Code Churn | Review Cycles | Throughput
  - All charts react to date picker changes
- [ ] Wire up repo selector if multiple repos onboarded

**Evening — Responsive + Polish**
- [ ] Test on different screen widths (desktop, tablet)
- [ ] Adjust Tailwind grid breakpoints
- [ ] **Commit:** `feat(frontend): add review cycles chart, health gauge, date picker, and dashboard layout`

**🧠 Learning Focus:** SVG drawing basics, URL-based state management (useSearchParams), CSS Grid responsive patterns

---

#### Day 12 (Fri): Repo Detail Page + Developer Breakdown
**Focus: Build the deep-dive view for individual repos.**

**Morning — Repo Detail Page (3 hours)**
- [ ] Build `RepoDetail.tsx`:
  - Header: repo name, stars, language, last synced, health gauge
  - Tab layout: Overview | Developers | Settings
  - Overview tab: all 4 charts scoped to this repo (same components, different data)
- [ ] Add "Sync Now" button — calls `POST /api/v1/repos/{id}/sync` (add this endpoint)
- [ ] Show sync status and last synced time

**Afternoon — Developer Metrics Table (3 hours)**
- [ ] Build Developers tab in `RepoDetail.tsx`:
  - Table columns: Developer | PRs Merged | Avg Latency (hrs) | Avg Churn | Review Rounds
  - Sortable columns (click header to sort)
  - Client-side sorting (data is small enough)
- [ ] Add mini sparkline charts per row (optional — stretch goal)
- [ ] Handle empty states (new repo with no data yet)

**Evening — Navigation Polish**
- [ ] Click repo card on Dashboard → navigates to RepoDetail
- [ ] Breadcrumb navigation: Dashboard > Repo Name
- [ ] Back button works correctly
- [ ] **Commit:** `feat(frontend): add repo detail page with developer breakdown table`

**🧠 Learning Focus:** Tab components, data tables with sorting, React Router params, navigation patterns

---

#### Day 13 (Sat): Basic Anomaly Detection (Statistical)
**Focus: Implement simple but effective anomaly detection without ML.**

**Morning — Z-Score Anomaly Service (3 hours)**
- [ ] Build `backend/app/services/anomaly_service.py`:
  ```python
  class AnomalyService:
      async def detect_anomalies(repo_id) -> list[Anomaly]:
          # For each metric (pr_latency, churn, review_rounds):
          # 1. Fetch last 30 days of daily values
          # 2. Compute rolling mean and std (14-day window)
          # 3. Flag any value > 2σ from rolling mean as anomaly
          # 4. Classify severity: >2σ = MEDIUM, >3σ = HIGH, >4σ = CRITICAL
          # 5. Insert into anomalies table

      async def get_anomalies(repo_id, severity, limit) -> list[Anomaly]

      async def run_detection_all_repos() -> DetectionSummary
  ```
- [ ] Define anomaly types:
  - `pr_latency_spike` — latency >2σ above rolling mean
  - `churn_surge` — daily churn >2σ above normal
  - `review_bottleneck` — review rounds or turnaround >2σ
  - `throughput_drop` — merged PRs significantly below rolling mean
- [ ] Wire into API: `GET /api/v1/anomalies?repo_id=&severity=`

**Afternoon — Anomaly Frontend (3 hours)**
- [ ] Build `useAnomalies.ts` hook
- [ ] Build `AnomalyTimeline.tsx`:
  - List view with severity color bars (red/orange/yellow)
  - Each card: type, metric name, expected vs actual, when detected
  - Click → navigate to repo detail with chart focused on that date
- [ ] Build `Anomalies.tsx` page — filterable feed
- [ ] Add anomaly count badge to sidebar navigation

**Evening — Integration**
- [ ] Run anomaly detection on a repo with real data
- [ ] Verify anomalies show up in dashboard and anomaly page
- [ ] Add anomaly count to Dashboard metric cards
- [ ] **Commit:** `feat: add statistical anomaly detection with z-score thresholds`

**🧠 Learning Focus:** Statistical anomaly detection (z-scores, rolling statistics), alert classification

---

#### Day 14 (Sun): Week 2 Review + Milestone 1 Prep
**Focus: Polish everything, fix bugs, prepare for deployment.**

- [ ] Full end-to-end walkthrough: onboard repo → view metrics → see anomalies
- [ ] Fix any visual bugs or data mismatches
- [ ] Add error boundaries to all pages
- [ ] Add loading skeletons to all data-dependent components
- [ ] Run test suite, fix failures
- [ ] Update `DEV_LOG.md` with Week 2 learnings
- [ ] **Commit:** `fix: Week 2 bug fixes and UI polish`
- [ ] **Push everything**

**Week 2 Checkpoint:**
```
✅ 5 metric computations (latency, churn, reviews, throughput, health score)
✅ 5 interactive chart components with date filtering
✅ Dashboard overview page with metric cards + chart grid
✅ Repo detail page with developer breakdown table
✅ Statistical anomaly detection (z-score based)
✅ Anomaly feed page with severity filtering
```

---

### WEEK 3 — DEPLOY + POLISH (Milestone 1 Complete)
**Goal:** Containerize, deploy to Cloud Run, CI/CD pipeline, documentation. End with a production URL.

**Deliverable by end of week:** Live URL anyone can visit, GitHub repo with green CI badge, comprehensive docs.

---

#### Day 15 (Mon): Docker + Local Production Build
**Focus: Containerize the app so it runs identically everywhere.**

**Morning — Backend Dockerfile (3 hours)**
- [ ] Write `backend/Dockerfile`:
  ```dockerfile
  # Stage 1: Build
  FROM python:3.11-slim as builder
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .

  # Stage 2: Runtime
  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /app .
  EXPOSE 8000
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
  ```
- [ ] Build and test: `docker build -t devscope-backend ./backend`
- [ ] Run: `docker run -p 8000:8000 --env-file .env devscope-backend`
- [ ] Verify all endpoints work from Docker container

**Afternoon — Frontend Build + Combined Serving (2 hours)**
- [ ] Build frontend: `cd frontend && npm run build`
- [ ] Option A (simpler): Serve frontend static files from FastAPI using `StaticFiles`
- [ ] Option B (cleaner): Separate Cloud Run services with CDN for frontend
- [ ] Start with Option A — add to FastAPI:
  ```python
  app.mount("/", StaticFiles(directory="static", html=True), name="static")
  ```
- [ ] Update Dockerfile to copy frontend build into backend image
- [ ] Test full app from single Docker container

**Evening — Docker Compose for Local Dev**
- [ ] Write `docker-compose.yml` for local development
- [ ] Verify `docker compose up` starts everything
- [ ] **Commit:** `chore(infra): add Dockerfile and docker-compose for containerized deployment`

**🧠 Learning Focus:** Multi-stage Docker builds, static file serving, Docker Compose, image optimization

---

#### Day 16 (Tue): Cloud Run Deployment
**Focus: Get a live URL.**

**Morning — Artifact Registry + Deploy (3 hours)**
- [ ] Enable Artifact Registry API in GCP
- [ ] Create Docker repository:
  ```bash
  gcloud artifacts repositories create devscope \
    --repository-format=docker \
    --location=us-central1
  ```
- [ ] Tag and push image:
  ```bash
  docker tag devscope-backend us-central1-docker.pkg.dev/PROJECT/devscope/backend:latest
  docker push us-central1-docker.pkg.dev/PROJECT/devscope/backend:latest
  ```
- [ ] Deploy to Cloud Run:
  ```bash
  gcloud run deploy devscope \
    --image=us-central1-docker.pkg.dev/PROJECT/devscope/backend:latest \
    --platform=managed \
    --region=us-central1 \
    --allow-unauthenticated \
    --set-env-vars="GCP_PROJECT_ID=...,BQ_DATASET=devscope" \
    --memory=512Mi \
    --min-instances=0 \
    --max-instances=3
  ```
- [ ] Test the live URL — verify all pages work

**Afternoon — Debugging + Config (2 hours)**
- [ ] Fix any deployment issues (CORS, env vars, service account permissions)
- [ ] Set up Cloud Run service account with BigQuery access
- [ ] Configure custom domain (optional — nice to have for resume)
- [ ] Test cold start times — optimize if >5s

**Evening — Monitoring**
- [ ] Check Cloud Run logs in GCP Console
- [ ] Verify structured logging shows up correctly
- [ ] Set up basic alerting (error rate, latency)
- [ ] **Commit:** `chore(infra): deploy to Cloud Run with Artifact Registry`

**🧠 Learning Focus:** Cloud Run deployment model, Artifact Registry, container orchestration, cold starts

**⚠️ Common Blockers:**
- Cloud Run can't access local `.env` file — set env vars via `--set-env-vars` or Secret Manager
- Service account on Cloud Run needs explicit BigQuery permissions
- CORS: update allowed origins to include your Cloud Run URL

---

#### Day 17 (Wed): GitHub Actions CI/CD
**Focus: Automate testing and deployment on every push.**

**Morning — CI Pipeline (3 hours)**
- [ ] Write `.github/workflows/ci.yml`:
  ```yaml
  name: CI
  on: [pull_request]
  jobs:
    backend-checks:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-python@v5
          with: { python-version: '3.11' }
        - run: pip install -r backend/requirements.txt -r backend/requirements-dev.txt
        - run: cd backend && ruff check app/
        - run: cd backend && pytest tests/unit/ -v

    frontend-checks:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: actions/setup-node@v4
          with: { node-version: '20' }
        - run: cd frontend && npm ci
        - run: cd frontend && npm run lint
        - run: cd frontend && npm run type-check
  ```
- [ ] Push a PR and verify CI runs green

**Afternoon — CD Pipeline (3 hours)**
- [ ] Write `.github/workflows/cd.yml`:
  ```yaml
  name: CD
  on:
    push: { branches: [main] }
  jobs:
    deploy:
      runs-on: ubuntu-latest
      steps:
        - uses: actions/checkout@v4
        - uses: google-github-actions/auth@v2
          with: { credentials_json: '${{ secrets.GCP_SA_KEY }}' }
        - uses: google-github-actions/setup-gcloud@v2
        - run: |
            gcloud builds submit --tag us-central1-docker.pkg.dev/$PROJECT/devscope/backend:${{ github.sha }}
            gcloud run deploy devscope --image=... --region=us-central1
  ```
- [ ] Add GCP service account key as GitHub secret
- [ ] Merge a PR to main → verify auto-deploy
- [ ] Add CI/CD status badges to README

**Evening — Branch Protection**
- [ ] Enable branch protection on `main`: require CI to pass before merge
- [ ] **Commit:** `ci: add GitHub Actions CI/CD pipelines`

**🧠 Learning Focus:** GitHub Actions syntax, CI/CD concepts, GCP authentication in CI, branch protection

---

#### Day 18 (Thu): Dark Mode + UI Polish
**Focus: Make the dashboard look professional.**

**Morning — Dark/Light Mode (2 hours)**
- [ ] Add theme toggle to Header
- [ ] Implement with Tailwind `dark:` classes
- [ ] Store preference in localStorage
- [ ] Update all components with dark variants
- [ ] Ensure charts look good in both themes

**Afternoon — UI Polish Sweep (3 hours)**
- [ ] Loading skeletons for every data-loading component
- [ ] Proper error boundaries with "retry" buttons
- [ ] Empty states with helpful messages ("No repos yet — add one to get started")
- [ ] Smooth page transitions
- [ ] Consistent spacing, typography, and color usage
- [ ] Favicon and page title
- [ ] Mobile responsiveness check (won't be perfect, but shouldn't break)

**Evening — Cross-Browser Check**
- [ ] Test in Chrome, Firefox, Safari
- [ ] Fix any visual inconsistencies
- [ ] **Commit:** `feat(frontend): add dark mode and comprehensive UI polish`

**🧠 Learning Focus:** Tailwind dark mode, CSS transitions, progressive enhancement

---

#### Day 19 (Fri): Documentation
**Focus: Write docs that make you look professional.**

**Morning — Technical Docs (3 hours)**
- [ ] Write `docs/architecture.md`:
  - System diagram (Mermaid) showing data flow
  - Technology choices with brief rationale
  - Component descriptions
- [ ] Write `docs/api-reference.md` (export from FastAPI OpenAPI, then annotate)
- [ ] Write `docs/data-model.md` — all BigQuery schemas with descriptions
- [ ] Write `docs/setup-guide.md` — step-by-step local dev setup

**Afternoon — README + ADRs (2 hours)**
- [ ] Polish `README.md`:
  - Project hero description
  - Architecture diagram
  - Screenshot/GIF of dashboard
  - Quick start instructions
  - Tech stack badges
  - CI/CD badge
  - Link to live demo
- [ ] Write 2-3 ADRs:
  - `001-bigquery-over-postgres.md` — why BQ for analytics
  - `002-statistical-anomalies-first.md` — why z-scores before ML
  - `003-fastapi-over-flask.md` — framework choice

**Evening — Final README Review**
- [ ] Read README as if you've never seen the project
- [ ] Does it clearly communicate what DevScope does, how to run it, and why it's impressive?
- [ ] **Commit:** `docs: add architecture, API reference, setup guide, and polished README`

---

#### Day 20 (Sat): Seed Data + Demo Prep
**Focus: Make sure anyone can try your project immediately.**

**Morning — Seed Data Polish (2 hours)**
- [ ] Improve `seed_data.py`:
  - Generate 90 days of realistic data for 3 sample repos
  - Include some anomalous periods (latency spikes, churn surges)
  - Include 8-10 developers per repo with varying patterns
- [ ] Add `make seed` command to Makefile
- [ ] Add instructions in README for seeding

**Afternoon — Demo Walkthrough (2 hours)**
- [ ] Do a complete fresh setup from clone → running (follow your own setup guide)
- [ ] Fix anything that's broken or unclear
- [ ] Record a short screen recording or take screenshots for README
- [ ] Prepare a 2-minute verbal demo walkthrough (for interviews)

**Evening — Final Checks**
- [ ] Run full test suite one more time
- [ ] Verify live deployment is working and stable
- [ ] **Commit:** `feat: polish seed data and demo preparation`

---

#### Day 21 (Sun): Milestone 1 Release
**Focus: Tag the release and celebrate.**

- [ ] Final review of all code
- [ ] Update CHANGELOG.md
- [ ] Create GitHub release: tag `v1.0.0` with release notes
- [ ] Update `DEV_LOG.md` with Week 3 summary
- [ ] **Push everything**
- [ ] Share the live URL — it's demo-ready!

**🎉 MILESTONE 1 COMPLETE — "DevScope Core"**
```
✅ GitHub API integration with pagination + rate limiting
✅ BigQuery data pipeline (6 tables, batch ingestion)
✅ 5 metric computations with analytical SQL
✅ FastAPI backend with 8+ endpoints + Swagger docs
✅ React/TypeScript dashboard with 5 interactive charts
✅ Repo detail page with developer breakdown
✅ Statistical anomaly detection with alert feed
✅ Dark/light mode, responsive layout, loading/error states
✅ Dockerized + deployed to Cloud Run
✅ CI/CD with GitHub Actions
✅ Comprehensive documentation
```

**This alone fully matches your resume description.** If you need to pause here for interviews or coursework, you have a complete, impressive project.

---

### ═══════════════════════════════════════════════════
### MILESTONE 2 — "DevScope Advanced" (Weeks 4–5)
### ═══════════════════════════════════════════════════

**Prerequisites:** Milestone 1 complete and deployed. You're now enhancing a working system.

---

### WEEK 4 — REAL-TIME PIPELINE
**Goal:** Events stream in real-time via GitHub Webhooks → Pub/Sub → Dataflow → BigQuery.

**Deliverable by end of week:** Opening a PR on a connected repo triggers real-time data flow, and the dashboard updates within seconds.

---

#### Day 22 (Mon): Pub/Sub Foundations
**Focus: Learn Pub/Sub concepts, set up topics and subscriptions.**

**Morning — Pub/Sub Setup (2 hours)**
- [ ] Enable Pub/Sub API in GCP
- [ ] Create topics:
  - `github-events` — main event stream
  - `github-events-dlq` — dead-letter queue for failed messages
- [ ] Create subscriptions:
  - `github-events-sub` — pull subscription on `github-events`
  - Configure: ack deadline 60s, dead-letter topic after 5 retries
- [ ] Update service account permissions: add Pub/Sub Publisher + Subscriber

**Afternoon — Publisher Client (3 hours)**
- [ ] Build `backend/app/core/pubsub_publisher.py`:
  ```python
  class PubSubPublisher:
      async def publish(topic, event_type, payload) -> str  # returns message_id
      async def publish_batch(topic, messages) -> list[str]
  ```
- [ ] Define message schema:
  ```json
  {
    "event_id": "uuid",
    "event_type": "PR_OPENED | PR_MERGED | REVIEW_SUBMITTED | COMMIT_PUSHED",
    "repo_id": "string",
    "timestamp": "ISO 8601",
    "data": { /* event-specific payload */ }
  }
  ```
- [ ] Add ordering key by `repo_id` (maintains event order per repo)
- [ ] Test: publish a message, verify in GCP Console

**Evening — Subscriber Worker (2 hours)**
- [ ] Build `backend/workers/event_processor.py`:
  - Pull messages from subscription
  - Parse, validate against schema
  - Route by event_type to appropriate handler
  - Ack on success, nack on failure
- [ ] Run publisher + subscriber locally, verify messages flow
- [ ] **Commit:** `feat(backend): add Pub/Sub publisher and subscriber for event streaming`

**🧠 Learning Focus:** Pub/Sub concepts (topics, subscriptions, ack/nack, dead-letter), message ordering, at-least-once delivery

---

#### Day 23 (Tue): GitHub Webhooks
**Focus: Receive real-time events from GitHub.**

**Morning — Webhook Endpoint (3 hours)**
- [ ] Build `backend/app/api/v1/webhooks.py`:
  ```python
  @router.post("/api/v1/webhooks/github")
  async def github_webhook(request: Request):
      # 1. Verify HMAC-SHA256 signature
      # 2. Parse X-GitHub-Event header
      # 3. Transform payload → internal event format
      # 4. Publish to Pub/Sub
      # 5. Return 200 OK
  ```
- [ ] Implement signature verification:
  ```python
  import hmac, hashlib
  expected = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()
  if not hmac.compare_digest(f"sha256={expected}", signature_header):
      raise HTTPException(403, "Invalid signature")
  ```
- [ ] Handle event types:
  - `pull_request` (actions: opened, closed, merged, reopened)
  - `pull_request_review` (actions: submitted)
  - `push` (commits to default branch)
- [ ] Transform each webhook payload → your standard event schema

**Afternoon — Local Testing with ngrok (2 hours)**
- [ ] Install ngrok, start tunnel: `ngrok http 8000`
- [ ] Add webhook to a test repo: Settings → Webhooks → add ngrok URL
- [ ] Select events: Pull requests, Pull request reviews, Pushes
- [ ] Open/close a PR → verify event arrives at your endpoint
- [ ] Check Pub/Sub Console — message published

**Evening — Wire to Processing Pipeline (2 hours)**
- [ ] Event processor picks up webhook-published messages
- [ ] Processor inserts/updates records in BigQuery
- [ ] Verify: open PR → webhook → Pub/Sub → processor → BigQuery → API can query it
- [ ] **Commit:** `feat(backend): add GitHub webhook receiver with signature verification`

**🧠 Learning Focus:** Webhook security (HMAC verification), ngrok tunneling, event transformation

**⚠️ Common Blockers:**
- Webhook signature: the raw body bytes matter — don't parse JSON before verifying
- ngrok free tier URL changes on restart — update webhook URL each time
- GitHub sends a `ping` event on webhook creation — handle it gracefully

---

#### Day 24 (Wed): Apache Beam — Learning Day
**Focus: Understand Beam's programming model before writing production code.**

**This is a dedicated learning day. Beam's abstraction is genuinely different from anything you've used before.**

**Morning — Concepts (3 hours)**
- [ ] Read: [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/)
- [ ] Understand core concepts:
  - **PCollection** — distributed dataset (like a list that can be processed in parallel)
  - **PTransform** — operation on a PCollection (Map, Filter, GroupByKey, etc.)
  - **Pipeline** — sequence of PTransforms
  - **Runner** — where the pipeline executes (DirectRunner local, DataflowRunner on GCP)
- [ ] Understand windowing:
  - **Fixed/Tumbling** — non-overlapping time buckets (every 24h)
  - **Sliding** — overlapping windows (1h window, sliding every 15min)
  - **Session** — gaps between events define window boundaries
  - **Triggers** — when to emit results from a window

**Afternoon — Tutorial Pipeline (3 hours)**
- [ ] Install: `pip install apache-beam[gcp]`
- [ ] Build a simple pipeline:
  ```python
  with beam.Pipeline(options=PipelineOptions()) as p:
      (p
       | 'Read' >> beam.io.ReadFromPubSub(subscription=sub)
       | 'Parse' >> beam.Map(json.loads)
       | 'Window' >> beam.WindowInto(window.FixedWindows(60))  # 1-min windows
       | 'Count' >> beam.combiners.Count.PerKey()
       | 'Print' >> beam.Map(print)
      )
  ```
- [ ] Run locally with DirectRunner
- [ ] Experiment: change window sizes, add filters, try GroupByKey

**Evening — Plan Production Pipeline**
- [ ] Sketch the actual DevScope pipeline on paper:
  ```
  Pub/Sub → Parse → Validate → Window(24h tumbling) →
  GroupByRepo → ComputeMetrics → WriteToBigQuery
  ```
- [ ] Identify custom PTransforms you'll need
- [ ] **Commit:** `docs: add Beam learning notes and pipeline design sketch`

**🧠 Learning Focus:** This is THE hardest learning day. Beam's windowing and trigger model is powerful but takes time to click. Don't rush it.

---

#### Day 25 (Thu): Dataflow Pipeline — Build
**Focus: Build the production pipeline for real-time metric aggregation.**

**Morning — Pipeline Implementation (4 hours)**
- [ ] Build `backend/dataflow/pipeline.py`:
  ```python
  def run():
      with beam.Pipeline(options=pipeline_options) as p:
          events = (
              p
              | 'ReadPubSub' >> beam.io.ReadFromPubSub(
                  subscription=SUBSCRIPTION,
                  with_attributes=True)
              | 'ParseJSON' >> beam.Map(parse_event)
              | 'ValidateSchema' >> beam.Filter(is_valid_event)
          )

          # 24-hour tumbling window for daily metrics
          daily_metrics = (
              events
              | 'DailyWindow' >> beam.WindowInto(
                  window.FixedWindows(86400),  # 24 hours
                  trigger=AfterWatermark(
                      early=AfterProcessingTime(300)),  # emit early every 5 min
                  accumulation_mode=AccumulationMode.ACCUMULATING)
              | 'KeyByRepo' >> beam.Map(lambda e: (e['repo_id'], e))
              | 'GroupByRepo' >> beam.GroupByKey()
              | 'ComputeMetrics' >> beam.ParDo(ComputeDailyMetrics())
              | 'WriteBQ' >> beam.io.WriteToBigQuery(
                  'daily_metrics',
                  write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND)
          )
  ```

**Afternoon — Custom Transforms (2 hours)**
- [ ] Build `backend/dataflow/transforms.py`:
  ```python
  class ComputeDailyMetrics(beam.DoFn):
      def process(self, element):
          repo_id, events = element
          pr_events = [e for e in events if e['event_type'].startswith('PR_')]
          # Compute: avg latency, total churn, review stats, throughput
          yield {
              'repo_id': repo_id,
              'metric_date': window_date,
              'metrics': computed_metrics
          }
  ```
- [ ] Handle late data gracefully (events arriving after window closes)

**Evening — Local Testing**
- [ ] Test with DirectRunner using sample Pub/Sub messages
- [ ] Verify metrics land in BigQuery
- [ ] **Commit:** `feat(pipeline): build Apache Beam pipeline for real-time metric aggregation`

---

#### Day 26 (Fri): Dataflow Deployment + E2E Testing
**Focus: Deploy pipeline to GCP Dataflow and test the full real-time flow.**

**Morning — Deploy to Dataflow (3 hours)**
- [ ] Update pipeline options for DataflowRunner:
  ```python
  pipeline_options = PipelineOptions([
      '--runner=DataflowRunner',
      '--project=YOUR_PROJECT',
      '--region=us-central1',
      '--temp_location=gs://devscope-temp/dataflow/',
      '--streaming',
      '--autoscaling_algorithm=THROUGHPUT_BASED',
      '--max_num_workers=3',
  ])
  ```
- [ ] Create GCS bucket for temp files
- [ ] Deploy: `python -m backend.dataflow.pipeline`
- [ ] Monitor in GCP Dataflow Console — verify job starts and runs

**Afternoon — End-to-End Real-Time Testing (3 hours)**
- [ ] Full flow test:
  1. Open a PR on connected repo
  2. GitHub sends webhook → your API receives it
  3. API publishes to Pub/Sub
  4. Dataflow pipeline processes the message
  5. Metrics update in BigQuery
  6. Dashboard shows new data
- [ ] Time the end-to-end latency (target: <30 seconds)
- [ ] Test with multiple events in quick succession

**Evening — Monitoring + Error Handling**
- [ ] Check Dataflow job metrics: throughput, latency, errors
- [ ] Verify dead-letter queue catches malformed messages
- [ ] Add Dataflow pipeline monitoring to docs
- [ ] **Commit:** `feat(pipeline): deploy Dataflow streaming pipeline to GCP`

**🧠 Learning Focus:** Dataflow deployment, streaming job monitoring, autoscaling, GCS staging

**⚠️ Common Blockers:**
- Dataflow jobs take 3-5 minutes to start — be patient
- Streaming jobs run continuously (and cost money) — stop when not testing
- Permission errors: Dataflow service account needs Pub/Sub Subscriber, BigQuery Writer, GCS access

---

#### Day 27 (Sat): Integration + Fallback Handling

**Morning — Graceful Degradation (2 hours)**
- [ ] If Dataflow is down, fall back to batch ingestion (already built in M1)
- [ ] Add health checks for pipeline status
- [ ] Dashboard should work regardless of whether real-time pipeline is running

**Afternoon — Dual-Mode Ingestion (2 hours)**
- [ ] Webhook events go through Pub/Sub → Dataflow (real-time)
- [ ] "Sync Now" button still triggers batch ingestion (backfill)
- [ ] Both paths write to the same BigQuery tables (idempotent by event_id)
- [ ] Test both paths work independently

**Evening — Week 4 Review**
- [ ] Run full test suite
- [ ] Update deployment docs with Dataflow instructions
- [ ] Update `DEV_LOG.md`
- [ ] **Commit:** `feat: add dual-mode ingestion with graceful degradation`

---

#### Day 28 (Sun): Week 4 Catch-Up
- [ ] Fix any remaining bugs from the week
- [ ] Refactor and clean up pipeline code
- [ ] **Push everything**

**Week 4 Checkpoint:**
```
✅ Pub/Sub topics + subscriptions configured
✅ GitHub webhook receiver with signature verification
✅ Real-time event flow: webhook → Pub/Sub → Dataflow → BigQuery
✅ Apache Beam pipeline deployed to Dataflow
✅ Dual-mode ingestion (real-time + batch fallback)
✅ End-to-end latency <30 seconds
```

---

### WEEK 5 — ML ANOMALY DETECTION + FINAL POLISH
**Goal:** Replace z-score anomalies with Vertex AI ML model, polish everything, ship v2.0.

**Deliverable by end of week:** ML-powered anomaly detection, upgraded dashboard, production v2.0 release.

---

#### Day 29 (Mon): Feature Engineering
**Focus: Prepare time-series features for ML training.**

**Morning — Feature Design (2 hours)**
- [ ] Build `backend/ml/preprocessing.py`:
  - Input: `daily_metrics` table (30-90 days of history per repo)
  - For each metric per repo, compute:
    - **Lag features:** value at t-1, t-7, t-14
    - **Rolling stats:** 7-day mean, std, min, max
    - **Trend:** linear slope over last 14 days
    - **Cyclical:** day-of-week (sin/cos encoding)
    - **Ratio features:** current / 7d-avg, current / 14d-avg

**Afternoon — Training Dataset (3 hours)**
- [ ] Export features from BigQuery → pandas DataFrame
- [ ] Generate labels:
  - Option A: Use your existing z-score anomalies as labels (>2σ = anomaly)
  - Option B: Manual labeling of known anomalous periods
- [ ] Train/validation split: **time-based** (train on first 70%, validate on last 30%)
- [ ] Save dataset to Cloud Storage as CSV
- [ ] Exploratory analysis: plot feature distributions, check for class imbalance

**Evening — Document Feature Pipeline**
- [ ] **Commit:** `feat(ml): add feature engineering pipeline for time-series anomaly detection`

**🧠 Learning Focus:** Time-series feature engineering, train/val splitting for temporal data, feature correlation analysis

---

#### Day 30 (Tue): Model Training
**Focus: Train and evaluate the anomaly detection model.**

**Morning — Model Training (3 hours)**
- [ ] Build `backend/ml/train.py`
- [ ] **Approach A — Vertex AI AutoML (recommended for first pass):**
  - Upload CSV dataset to Vertex AI
  - Create TabularDataset
  - Launch AutoML training job (classification: anomaly vs normal)
  - Wait for training to complete (~1-2 hours)
- [ ] **Approach B — Custom Model (if you want more control):**
  ```python
  from sklearn.ensemble import IsolationForest
  model = IsolationForest(contamination=0.05, random_state=42)
  model.fit(X_train)
  predictions = model.predict(X_val)
  ```
  - Package as a custom container for Vertex AI

**Afternoon — Evaluation (2 hours)**
- [ ] Evaluate on validation set:
  - Precision, Recall, F1 at various thresholds
  - Confusion matrix
  - Precision-Recall curve
- [ ] Compare against your z-score baseline — ML should be more nuanced
- [ ] Log all metrics

**Evening — Save Model**
- [ ] Save model to Cloud Storage
- [ ] Register in Vertex AI Model Registry
- [ ] **Commit:** `feat(ml): train anomaly detection model with Vertex AI`

**🧠 Learning Focus:** Vertex AI training workflow, model evaluation metrics, IsolationForest algorithm

---

#### Day 31 (Wed): Prediction Endpoint + Integration
**Focus: Deploy model and wire predictions into the app.**

**Morning — Deploy Endpoint (3 hours)**
- [ ] Deploy model to Vertex AI online prediction endpoint:
  ```bash
  gcloud ai endpoints deploy-model ENDPOINT_ID \
    --model=MODEL_ID \
    --display-name=devscope-anomaly \
    --traffic-split=0=100
  ```
- [ ] Build `backend/app/core/vertex_client.py`:
  ```python
  class VertexClient:
      async def predict(features: dict) -> AnomalyPrediction
      async def predict_batch(feature_list: list) -> list[AnomalyPrediction]
  ```
- [ ] Test endpoint: send sample features, verify prediction response

**Afternoon — Upgrade Anomaly Service (3 hours)**
- [ ] Update `anomaly_service.py`:
  - Fetch latest features from BigQuery
  - Call Vertex AI endpoint for predictions
  - Parse confidence scores
  - Categorize: type + severity based on confidence
  - Insert into `anomalies` table
- [ ] Keep z-score as fallback if Vertex AI endpoint is unavailable
- [ ] Set up Cloud Scheduler for hourly detection runs:
  ```bash
  gcloud scheduler jobs create http detect-anomalies \
    --schedule="0 * * * *" \
    --uri="https://devscope-HASH.run.app/api/v1/anomalies/detect" \
    --http-method=POST
  ```

**Evening — Verify**
- [ ] Run detection, verify ML anomalies appear in API
- [ ] Compare ML anomalies vs z-score anomalies — note differences
- [ ] **Commit:** `feat(ml): deploy Vertex AI prediction endpoint and integrate with anomaly service`

**🧠 Learning Focus:** Vertex AI endpoint deployment, online vs batch prediction, Cloud Scheduler

---

#### Day 32 (Thu): Dashboard Upgrades
**Focus: Surface ML anomalies with confidence scores on the dashboard.**

**Morning — Enhanced Anomaly UI (3 hours)**
- [ ] Upgrade `AnomalyTimeline.tsx`:
  - Show confidence percentage for each anomaly
  - Add "ML-detected" vs "Rule-based" badges
  - Expected vs actual value comparison bar
  - "Resolve" button to dismiss false positives
- [ ] Add anomaly overlay to charts:
  - Recharts `ReferenceArea` for anomalous time periods (semi-transparent red/yellow)
  - Tooltip shows anomaly details when hovering over flagged regions

**Afternoon — Dashboard Enhancements (3 hours)**
- [ ] Add real-time indicator: "Last updated X seconds ago" with auto-refresh
- [ ] Add notification bell: dropdown with recent anomalies
- [ ] Improve health score gauge: show sub-metric breakdown on hover
- [ ] Add "Compare Repos" view (side-by-side metrics for 2 repos)

**Evening — Polish**
- [ ] Smooth animations for data updates
- [ ] Consistent styling for ML vs statistical anomalies
- [ ] **Commit:** `feat(frontend): upgrade anomaly UI with ML confidence scores and chart overlays`

---

#### Day 33 (Fri): Testing + Performance
**Focus: Comprehensive testing and performance optimization.**

**Morning — Test Suite (3 hours)**
- [ ] Backend unit tests: all services, clients, API endpoints
- [ ] Frontend: component tests for key pages (Dashboard, RepoDetail, Anomalies)
- [ ] Integration test: full pipeline end-to-end
- [ ] Load test: can the API handle 100 concurrent metric queries?

**Afternoon — Performance (2 hours)**
- [ ] Backend: add response caching for expensive BigQuery queries (TTL: 5min)
- [ ] Frontend: verify React Query caching works correctly
- [ ] Check BigQuery query costs — optimize expensive queries
- [ ] Reduce Docker image size (remove dev dependencies, use slim base)
- [ ] Verify Cloud Run cold start is acceptable

**Evening — Bug Fixes**
- [ ] Fix any issues found during testing
- [ ] **Commit:** `test: add comprehensive test suite and performance optimizations`

---

#### Day 34 (Sat): Final Documentation + Release
**Focus: Ship v2.0.**

**Morning — Documentation Updates (2 hours)**
- [ ] Update `docs/architecture.md` with Milestone 2 components (Pub/Sub, Dataflow, Vertex AI)
- [ ] Add new ADRs:
  - `004-pubsub-over-kafka.md`
  - `005-vertex-ai-anomaly-detection.md`
- [ ] Update `docs/deployment.md` with Dataflow + Vertex AI deployment steps
- [ ] Update README with new architecture diagram and screenshots

**Afternoon — Release (2 hours)**
- [ ] Deploy final version to Cloud Run
- [ ] Verify everything works on production
- [ ] Update CHANGELOG.md
- [ ] Tag `v2.0.0` with detailed release notes
- [ ] Write final `DEV_LOG.md` entry

**Evening — Celebrate**
- [ ] **Push everything**
- [ ] You're done! 🎉

---

#### Day 35 (Sun): Buffer Day
- [ ] Catch-up on anything from the week
- [ ] Optional stretch goals:
  - [ ] GitHub OAuth login (replace PAT with proper OAuth flow)
  - [ ] Email/Slack notifications for critical anomalies
  - [ ] Terraform IaC for all GCP resources
  - [ ] API key authentication for multi-user support

**🎉 MILESTONE 2 COMPLETE — "DevScope Advanced"**
```
✅ Everything from Milestone 1, PLUS:
✅ Real-time GitHub webhooks → Pub/Sub → Dataflow pipeline
✅ Apache Beam streaming with windowed aggregation
✅ Vertex AI anomaly detection with confidence scores
✅ ML vs rule-based anomaly comparison
✅ Enhanced dashboard with chart overlays and real-time updates
✅ Cloud Scheduler for automated hourly detection
✅ Comprehensive test suite
✅ Full production deployment with CI/CD
```

---

## 6. PROJECT MANAGEMENT SETUP

### GitHub Project Board (Kanban)
Create a GitHub Project with these columns:
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
component:pipeline   — Data pipeline / Pub/Sub / Dataflow
component:ml         — ML / Vertex AI
component:infra      — Docker, CI/CD, GCP config

milestone:core       — Milestone 1
milestone:advanced   — Milestone 2
```

### Branch Strategy
```
main                 — Production-ready, protected
dev                  — Integration branch
feature/GH-{num}-*   — Feature branches (e.g., feature/GH-12-pr-latency-chart)
fix/GH-{num}-*       — Bug fix branches
```

### Commit Convention (Conventional Commits)
```
feat(backend): add PR latency metric computation
fix(frontend): correct date range filter timezone handling
chore(infra): update Dockerfile base image
docs: add BigQuery schema documentation
test(backend): add metrics service unit tests
```

### PR Template
```markdown
## What
<!-- Brief description of changes -->

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
```

### Daily Dev Log Template (`DEV_LOG.md`)
```markdown
## Day X — YYYY-MM-DD

### Goals
- [ ] Goal 1
- [ ] Goal 2

### Completed
- What I built
- Key decisions made

### Blockers
- Issues encountered and how I solved them

### Learnings
- New concepts / techniques learned

### Tomorrow
- Plan for next session
```

---

## 7. KEY TECHNICAL CONCEPTS BY WEEK

**Week 1 (Foundation):**
- FastAPI async patterns, dependency injection, middleware
- GitHub API (REST + pagination, rate limits)
- BigQuery SDK (schema definition, streaming inserts, parameterized queries)
- React project architecture (feature-based folder structure)
- React Router v6, React Query basics

**Week 2 (Metrics + Dashboard):**
- Analytical SQL (window functions, CTEs, PERCENTILE_CONT, DATE_TRUNC)
- Recharts for data visualization (AreaChart, BarChart, custom tooltips)
- React Query advanced (stale time, cache invalidation, dependent queries)
- SVG basics for custom gauge components
- Data table patterns (sorting, pagination)

**Week 3 (Deploy + Polish):**
- Docker multi-stage builds, image optimization
- Cloud Run (scaling, concurrency, cold starts, env vars)
- GitHub Actions (workflow syntax, secrets, artifacts)
- Tailwind dark mode, responsive design
- Technical writing, system documentation, ADRs

**Week 4 (Real-Time):**
- Pub/Sub messaging (topics, subscriptions, ack/nack, dead-letter)
- Webhook security (HMAC signature verification)
- Apache Beam programming model (PCollections, windowing, triggers)
- GCP Dataflow deployment and monitoring
- Event-driven architecture patterns

**Week 5 (ML):**
- Time-series feature engineering (lags, rolling stats, trends)
- Anomaly detection algorithms (Isolation Forest, z-scores)
- Vertex AI (training, deployment, prediction endpoints)
- Cloud Scheduler for automation
- ML pipeline orchestration

---

## 8. ENVIRONMENT VARIABLES (.env.example)

```env
# ─── GitHub ────────────────────────────────────────
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_CLIENT_ID=your-oauth-client-id
GITHUB_CLIENT_SECRET=your-oauth-client-secret

# ─── GCP ───────────────────────────────────────────
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# ─── BigQuery ──────────────────────────────────────
BQ_DATASET=devscope
BQ_LOCATION=US

# ─── Pub/Sub (Milestone 2) ────────────────────────
PUBSUB_TOPIC_EVENTS=github-events
PUBSUB_TOPIC_DLQ=github-events-dlq
PUBSUB_SUBSCRIPTION=github-events-sub

# ─── Vertex AI (Milestone 2) ──────────────────────
VERTEX_ENDPOINT_ID=your-endpoint-id
VERTEX_MODEL_ID=your-model-id

# ─── App ───────────────────────────────────────────
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 9. MAKEFILE REFERENCE

```makefile
.PHONY: dev test lint format setup seed

# ─── Setup ─────────────────────────────────────────
setup:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install

# ─── Development ───────────────────────────────────
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	make -j2 dev-backend dev-frontend

# ─── Testing ───────────────────────────────────────
test-backend:
	cd backend && pytest -v --cov=app

test-frontend:
	cd frontend && npm run test

test:
	make test-backend && make test-frontend

# ─── Quality ───────────────────────────────────────
lint:
	cd backend && ruff check app/
	cd frontend && npm run lint

format:
	cd backend && ruff format app/
	cd frontend && npm run format

type-check:
	cd frontend && npm run type-check

# ─── Data ──────────────────────────────────────────
seed:
	cd backend && python scripts/seed_data.py

backfill:
	cd backend && python scripts/run_backfill.py

# ─── Docker ────────────────────────────────────────
build:
	docker build -t devscope-backend ./backend

run:
	docker run -p 8000:8000 --env-file .env devscope-backend

# ─── Deploy ────────────────────────────────────────
deploy:
	gcloud builds submit --tag us-central1-docker.pkg.dev/$(GCP_PROJECT_ID)/devscope/backend:latest ./backend
	gcloud run deploy devscope --image=us-central1-docker.pkg.dev/$(GCP_PROJECT_ID)/devscope/backend:latest --region=us-central1
```

---

## 10. QUICK-START CHECKLIST (Do These Before Day 1)

### Accounts & Access
- [ ] GitHub account with a Personal Access Token (classic, `repo` + `read:org` scopes)
- [ ] GCP account with billing enabled (free tier has $300 credit for 90 days)
- [ ] Create GCP project

### GCP Setup
- [ ] Enable APIs: BigQuery, Cloud Run, Artifact Registry
- [ ] Create service account: BigQuery Admin + Cloud Run Admin roles
- [ ] Download service account JSON key
- [ ] Install `gcloud` CLI: `gcloud auth login && gcloud config set project YOUR_PROJECT_ID`

### Local Tools
- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] Docker Desktop installed and running
- [ ] Git configured with SSH key
- [ ] VS Code with extensions: Python, ESLint, Tailwind CSS IntelliSense, Prettier

### Bookmarks
- [ ] [GitHub REST API docs](https://docs.github.com/en/rest)
- [ ] [BigQuery SQL reference](https://cloud.google.com/bigquery/docs/reference/standard-sql/query-syntax)
- [ ] [FastAPI docs](https://fastapi.tiangolo.com)
- [ ] [Recharts docs](https://recharts.org/en-US)
- [ ] [React Query docs](https://tanstack.com/query/latest)
- [ ] [Tailwind CSS docs](https://tailwindcss.com/docs)
- [ ] [Apache Beam Python SDK](https://beam.apache.org/documentation/sdks/python/) (for Week 4)
- [ ] [Vertex AI docs](https://cloud.google.com/vertex-ai/docs) (for Week 5)

---

## 11. COST ESTIMATES (GCP Free Tier)

| Service | Free Tier | DevScope Usage (Dev) | Monthly Cost |
|---------|-----------|---------------------|--------------|
| BigQuery | 1TB queries/month, 10GB storage | ~5-20GB queries, <1GB storage | $0 |
| Cloud Run | 2M requests, 360K vCPU-seconds | ~1K requests/day dev | $0 |
| Pub/Sub | 10GB/month | <1GB | $0 |
| Dataflow | None (pay per use) | ~$1-5/hour when running | **$5-20** (only run during testing) |
| Vertex AI | $300 free credit | Training: ~$2-10, Endpoint: ~$1/hour | **$10-30** (stop endpoint when not testing) |
| Artifact Registry | 500MB free | ~200MB | $0 |

**Total estimated cost: $15-50 for the entire project** (mostly Dataflow + Vertex AI in Weeks 4-5)

**Cost-saving tips:**
- Stop Dataflow streaming jobs when not actively testing
- Delete Vertex AI endpoints when not in use (redeploy when needed)
- Use DirectRunner (local) for Beam development, only deploy to Dataflow for integration testing
- Monitor billing daily during Weeks 4-5
