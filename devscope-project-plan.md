# DevScope — Repository Intelligence Tool
## Complete Project Plan & Build Guide

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

## 2. INDUSTRY-STANDARD PROJECT STRUCTURE

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
│   │   │   │   └── webhooks.py       # /api/v1/webhooks — GitHub webhook receiver
│   │   │
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── github_client.py      # GitHub API wrapper (REST + GraphQL)
│   │   │   ├── pubsub_publisher.py   # Pub/Sub message publishing
│   │   │   ├── bigquery_client.py    # BigQuery read/write operations
│   │   │   └── vertex_client.py      # Vertex AI inference client
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
│   │   ├── event_processor.py        # Pub/Sub subscriber — processes events
│   │   └── batch_ingester.py         # Historical data backfill worker
│   │
│   ├── dataflow/
│   │   ├── pipeline.py               # Apache Beam pipeline definition
│   │   └── transforms.py             # Custom PTransforms for metric aggregation
│   │
│   ├── ml/
│   │   ├── train.py                  # Vertex AI training job script
│   │   ├── predict.py                # Batch/online prediction
│   │   └── preprocessing.py          # Feature engineering for time series
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
└── CHANGELOG.md                      # Version history
```

---

## 3. COMPLETE FEATURE LIST

### 3.1 — GitHub Integration
- [ ] GitHub OAuth2 app registration + token management
- [ ] REST API client with automatic rate-limit handling (retry + backoff)
- [ ] GraphQL client for batch queries (PRs, reviews, commits)
- [ ] Webhook receiver for real-time push events (PR opened, merged, review submitted)
- [ ] Repository onboarding flow (connect → validate → start ingestion)
- [ ] Support for org-level and individual repo connections
- [ ] Historical data backfill (paginate through past PRs/commits)

### 3.2 — Data Ingestion & Streaming
- [ ] Pub/Sub topic creation and message publishing
- [ ] Message schema definition (Avro or JSON schema)
- [ ] Event types: PR_OPENED, PR_MERGED, PR_CLOSED, REVIEW_SUBMITTED, COMMIT_PUSHED
- [ ] Dead-letter topic for failed messages
- [ ] Pub/Sub subscriber worker for event processing
- [ ] Idempotent message handling (deduplication by event ID)
- [ ] Batch vs streaming ingestion modes

### 3.3 — Data Storage (BigQuery)
- [ ] Schema design for tables: `raw_events`, `pull_requests`, `commits`, `reviews`, `daily_metrics`, `anomalies`
- [ ] Partitioned tables (by date) for query performance
- [ ] Clustered tables (by repo_id) for efficient filtering
- [ ] Materialized views for pre-aggregated metrics
- [ ] Data retention policies (raw events: 90 days, aggregated: unlimited)
- [ ] Seed script with realistic sample data

### 3.4 — Metric Computation
- [ ] **PR Latency** — time from PR open to first review, to approval, to merge
- [ ] **Code Churn** — lines added vs deleted per PR, rework ratio
- [ ] **Review Cycles** — number of review rounds per PR, review turnaround time
- [ ] **Deployment Frequency** — merges to main per day/week
- [ ] **Throughput** — PRs merged per developer per week
- [ ] **Health Score** — composite 0-100 score from weighted sub-metrics
- [ ] Time-windowed aggregations (daily, weekly, monthly)
- [ ] Per-developer and per-repo metric breakdowns

### 3.5 — Stream Processing (Cloud Dataflow)
- [ ] Apache Beam pipeline for real-time metric aggregation
- [ ] Sliding window computations (1h, 24h, 7d rolling metrics)
- [ ] Tumbling window for daily snapshots
- [ ] Side inputs for repo metadata enrichment
- [ ] Pipeline monitoring and error handling
- [ ] Autoscaling configuration

### 3.6 — Anomaly Detection (Vertex AI)
- [ ] Feature engineering for time-series data (lag features, rolling stats)
- [ ] Training pipeline: historical metric data → Vertex AI AutoML or custom model
- [ ] Online prediction endpoint deployment
- [ ] Anomaly types: PR latency spike, churn surge, review bottleneck
- [ ] Confidence scores for each detected anomaly
- [ ] Scheduled retraining job (weekly)
- [ ] Alert generation for high-confidence anomalies

### 3.7 — Backend API (FastAPI)
- [ ] `POST /api/v1/repos` — onboard new repository
- [ ] `GET /api/v1/repos` — list connected repos
- [ ] `GET /api/v1/repos/{id}` — repo detail
- [ ] `DELETE /api/v1/repos/{id}` — disconnect repo
- [ ] `GET /api/v1/metrics?repo_id=&window=&group_by=` — query metrics
- [ ] `GET /api/v1/metrics/{repo_id}/health` — health score
- [ ] `GET /api/v1/anomalies?repo_id=&severity=` — anomaly feed
- [ ] `POST /api/v1/webhooks/github` — webhook receiver
- [ ] `GET /api/v1/health` — service healthcheck
- [ ] API key or OAuth authentication middleware
- [ ] Request validation, error handling, structured logging
- [ ] OpenAPI/Swagger documentation auto-generation
- [ ] CORS configuration

### 3.8 — Frontend Dashboard (React/TypeScript)
- [ ] **Onboarding page** — GitHub OAuth → select repos → start ingestion
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

### 3.9 — Deployment & DevOps
- [ ] Backend Dockerfile (multi-stage build)
- [ ] Frontend build → Cloud Storage or bundled with backend
- [ ] Cloud Run service deployment (backend)
- [ ] GitHub Actions CI pipeline (lint, test, type-check)
- [ ] GitHub Actions CD pipeline (build, push image, deploy)
- [ ] Environment variable management (.env.example)
- [ ] Makefile for common commands
- [ ] Health check endpoint for Cloud Run

---

## 4. WEEK-BY-WEEK BUILD PLAN

### PHASE 1 — FOUNDATION (Days 1–3)
**Goal:** Local dev running, GitHub data flowing, stored somewhere queryable.

#### Day 1: Project Setup + GitHub Client
**Morning — Scaffolding**
- [ ] Initialize git repo, create branch strategy (main → dev → feature/*)
- [ ] Set up backend: `mkdir -p backend/app/{api/v1,core,services,models,utils}`
- [ ] Create `pyproject.toml`, `requirements.txt` (fastapi, uvicorn, httpx, google-cloud-bigquery, google-cloud-pubsub, pydantic-settings, pytest)
- [ ] Set up frontend: `npm create vite@latest frontend -- --template react-ts`
- [ ] Install frontend deps: tailwindcss, react-router-dom, @tanstack/react-query, recharts, axios
- [ ] Create `.env.example` with all required vars
- [ ] Write initial `README.md` with project description
- [ ] Create `Makefile` with `dev`, `test`, `lint`, `format` targets

**Afternoon — GitHub API Client**
- [ ] Register a GitHub OAuth App (or use Personal Access Token for dev)
- [ ] Build `github_client.py` — wrapper class with:
  - `get_repo(owner, name)` — fetch repo metadata
  - `list_pull_requests(owner, name, state, per_page, page)` — paginated PR list
  - `get_pull_request(owner, name, number)` — single PR with review data
  - `list_commits(owner, name, since, until)` — commit history
  - `list_reviews(owner, name, pr_number)` — reviews for a PR
- [ ] Implement rate limit detection (check `X-RateLimit-Remaining` header)
- [ ] Add exponential backoff retry logic
- [ ] Write unit tests with mocked HTTP responses

**Learning Focus:** FastAPI project structure, httpx async HTTP client, GitHub API pagination

---

#### Day 2: Data Models + BigQuery Setup
**Morning — BigQuery Schemas**
- [ ] Create GCP project (or use existing free tier)
- [ ] Enable BigQuery API
- [ ] Design and create tables:
  ```
  devscope.raw_events          — every GitHub event (partitioned by event_date)
  devscope.pull_requests       — enriched PR records (partitioned by created_date)
  devscope.commits             — commit records
  devscope.reviews             — review records
  devscope.daily_metrics       — pre-aggregated daily stats (partitioned by metric_date)
  devscope.anomalies           — detected anomalies
  ```
- [ ] Build `bigquery_client.py` — insert rows, run queries, create tables
- [ ] Write `seed_data.py` — generate 30 days of realistic sample data

**Afternoon — Ingestion Service**
- [ ] Build `ingestion_service.py`:
  - `ingest_repo(owner, name)` — full historical backfill
  - `ingest_prs(owner, name, since)` — incremental PR fetch
  - `ingest_commits(owner, name, since)` — incremental commits
- [ ] Transform GitHub API responses → BigQuery row format
- [ ] Handle pagination (follow `Link` headers or GraphQL cursors)
- [ ] Add structured logging throughout
- [ ] Test with a real public repo (e.g., facebook/react)

**Learning Focus:** BigQuery table design (partitioning, clustering), GCP SDK, data pipeline patterns

---

#### Day 3: FastAPI Endpoints + Basic Frontend Shell
**Morning — API Layer**
- [ ] Build `main.py` with FastAPI app, CORS middleware, lifespan events
- [ ] Create Pydantic schemas (`schemas.py`) for all request/response models
- [ ] Implement endpoints:
  - `POST /api/v1/repos` — trigger ingestion for a repo
  - `GET /api/v1/repos` — list onboarded repos
  - `GET /api/v1/repos/{repo_id}` — repo details
  - `GET /api/v1/health` — healthcheck
- [ ] Add error handling middleware (custom exception handlers)
- [ ] Verify Swagger UI at `/docs`
- [ ] Write integration tests for endpoints

**Afternoon — Frontend Shell**
- [ ] Set up routing: `/`, `/repos/:id`, `/anomalies`, `/settings`
- [ ] Build `DashboardLayout.tsx` — sidebar + header + content area
- [ ] Build `Sidebar.tsx` — navigation links with active state
- [ ] Build `Header.tsx` — app title, user avatar placeholder
- [ ] Create API client (`client.ts`) with base URL config
- [ ] Build `Onboarding.tsx` — form to input repo owner/name, calls POST /repos
- [ ] Display repo list on dashboard from GET /repos
- [ ] Add loading spinners and error states

**Learning Focus:** FastAPI dependency injection, Pydantic validation, React Router v6, component architecture

---

### PHASE 2 — METRICS ENGINE (Days 4–6)
**Goal:** Compute real metrics from ingested data, display on interactive charts.

#### Day 4: Metric Computation
**Morning — Metrics Service**
- [ ] Build `metrics_service.py` with SQL-based metric queries:
  - `get_pr_latency(repo_id, window)` — median/p95 time to first review, to merge
  - `get_code_churn(repo_id, window)` — additions, deletions, net churn per day
  - `get_review_cycles(repo_id, window)` — avg review rounds, turnaround time
  - `get_throughput(repo_id, window)` — PRs merged per week
  - `get_health_score(repo_id)` — weighted composite of all metrics
- [ ] Write BigQuery SQL queries (use parameterized queries for safety)
- [ ] Implement time-window filtering (7d, 30d, 90d, custom)
- [ ] Add caching layer (in-memory TTL cache for repeated queries)

**Afternoon — Metrics API**
- [ ] Implement `GET /api/v1/metrics?repo_id=&metric=&window=`
- [ ] Implement `GET /api/v1/metrics/{repo_id}/health`
- [ ] Add `group_by` parameter (developer, week, repo)
- [ ] Response format: `{ metric, values: [{ date, value }], summary: { avg, p50, p95, trend } }`
- [ ] Test with seeded data — verify SQL accuracy

**Learning Focus:** Analytical SQL (window functions, CTEs, percentiles), caching strategies, API design

---

#### Day 5: Dashboard Charts
**Morning — Chart Components**
- [ ] Build `useMetrics.ts` hook — React Query wrapper for metrics endpoint
- [ ] Build `PRLatencyChart.tsx` — line chart (Recharts) showing median + p95 over time
- [ ] Build `CodeChurnChart.tsx` — stacked area chart (additions green, deletions red)
- [ ] Build `ReviewCycleChart.tsx` — bar chart of review round distribution
- [ ] Build `MetricCard.tsx` — summary stat with trend arrow (↑ or ↓)

**Afternoon — Dashboard Assembly**
- [ ] Build `Dashboard.tsx`:
  - Row of MetricCards at top (total PRs, avg latency, health score, active anomalies)
  - Grid of charts below (2×2 layout)
  - Date range picker affecting all charts
- [ ] Build `DateRangePicker.tsx` — preset buttons (7d, 30d, 90d) + custom range
- [ ] Wire up all charts to live API data
- [ ] Add responsive breakpoints

**Learning Focus:** Recharts API, React Query patterns, responsive CSS Grid with Tailwind

---

#### Day 6: Repo Detail Page + Developer Breakdown
**Morning — Repo Detail**
- [ ] Build `RepoDetail.tsx`:
  - Repo header (name, stars, last updated, health gauge)
  - Tab layout: Overview | PRs | Developers | Settings
  - Overview tab: all charts scoped to this repo
- [ ] Build `HealthScoreGauge.tsx` — radial gauge component (SVG-based)
- [ ] Add drill-down: click a data point → show individual PRs

**Afternoon — Developer Metrics**
- [ ] Add `GET /api/v1/metrics/{repo_id}/developers` endpoint
- [ ] Build contributor table: developer, PRs merged, avg review time, churn
- [ ] Sortable columns, pagination
- [ ] Build sparkline mini-charts per developer row

**Learning Focus:** SVG custom components, data tables with sorting, tab-based navigation

---

### PHASE 3 — REAL-TIME PIPELINE (Days 7–9)
**Goal:** Events stream in real-time via Pub/Sub, processed by Dataflow.

#### Day 7: Pub/Sub Integration
**Morning — Publisher**
- [ ] Enable Pub/Sub API in GCP
- [ ] Create topics: `github-events`, `github-events-dlq`
- [ ] Build `pubsub_publisher.py`:
  - `publish_event(topic, event_type, payload)` — publish with attributes
  - Message format: JSON with `event_id`, `event_type`, `repo_id`, `timestamp`, `data`
- [ ] Add Pub/Sub publishing to ingestion service (dual-write: BigQuery + Pub/Sub)

**Afternoon — Subscriber Worker**
- [ ] Build `event_processor.py` — Pub/Sub pull subscriber
- [ ] Process messages: parse, validate, compute incremental metrics, write to BigQuery
- [ ] Implement idempotent handling (check event_id before processing)
- [ ] Add dead-letter queue routing for failed messages
- [ ] Handle acknowledgement properly (ack only after successful processing)

**Learning Focus:** Pub/Sub concepts (topics, subscriptions, ack deadlines), event-driven architecture

---

#### Day 8: GitHub Webhooks
**Morning — Webhook Receiver**
- [ ] Build `POST /api/v1/webhooks/github`:
  - Verify webhook signature (HMAC-SHA256)
  - Parse event type from `X-GitHub-Event` header
  - Transform webhook payload → internal event format
  - Publish to Pub/Sub
- [ ] Handle event types: `pull_request`, `pull_request_review`, `push`
- [ ] Add webhook secret to config

**Afternoon — End-to-End Real-Time Flow**
- [ ] Configure webhook on a test repo (use ngrok for local dev)
- [ ] Open a PR → verify event flows: GitHub → webhook → Pub/Sub → worker → BigQuery
- [ ] Verify dashboard updates with new data
- [ ] Add retry logic for transient failures
- [ ] Monitor with structured logging

**Learning Focus:** Webhook security (signature verification), ngrok tunneling, event-driven debugging

---

#### Day 9: Cloud Dataflow Pipeline
**Morning — Apache Beam Basics**
- [ ] Install `apache-beam[gcp]`
- [ ] Build `pipeline.py`:
  - Read from Pub/Sub subscription
  - Parse and validate messages
  - Apply windowing (sliding 1h, tumbling 24h)
  - Aggregate metrics per window
  - Write aggregated results to BigQuery `daily_metrics` table
- [ ] Build custom `PTransform`s in `transforms.py`:
  - `ComputePRLatency` — calculate time deltas
  - `ComputeCodeChurn` — sum additions/deletions
  - `AggregateByWindow` — group and compute stats

**Afternoon — Pipeline Testing & Deployment**
- [ ] Test pipeline locally with DirectRunner
- [ ] Deploy to Dataflow (DataflowRunner) — configure autoscaling
- [ ] Monitor pipeline in GCP Console
- [ ] Verify end-to-end: webhook → Pub/Sub → Dataflow → BigQuery → API → dashboard

**Learning Focus:** Apache Beam programming model (PCollections, PTransforms, windowing), GCP Dataflow

---

### PHASE 4 — ML & ANOMALY DETECTION (Days 10–12)
**Goal:** Train anomaly detection model, deploy predictions, surface alerts.

#### Day 10: Feature Engineering + Training
**Morning — Feature Prep**
- [ ] Build `preprocessing.py`:
  - Extract time-series features from `daily_metrics`
  - Lag features (1d, 7d, 14d lookback)
  - Rolling statistics (7d mean, std, min, max)
  - Day-of-week encoding
  - Trend features (linear slope over 14d window)
- [ ] Export training dataset to Cloud Storage (CSV/Parquet)

**Afternoon — Model Training**
- [ ] Build `train.py`:
  - Option A: Vertex AI AutoML Tabular (easiest — upload dataset, auto-train)
  - Option B: Custom training with scikit-learn IsolationForest or Prophet
- [ ] Define anomaly labels (derive from historical data — top 5% extreme values)
- [ ] Train/val split (time-based, not random)
- [ ] Log metrics: precision, recall, F1 at various thresholds
- [ ] Save model artifacts to Cloud Storage

**Learning Focus:** Time-series feature engineering, anomaly detection algorithms, Vertex AI training

---

#### Day 11: Prediction Pipeline + Anomaly API
**Morning — Predictions**
- [ ] Deploy model to Vertex AI endpoint (or use batch prediction)
- [ ] Build `predict.py`:
  - Fetch latest features from BigQuery
  - Call Vertex AI endpoint
  - Parse predictions → anomaly records with confidence scores
  - Write to `anomalies` table
- [ ] Build `anomaly_service.py`:
  - `detect_anomalies(repo_id)` — run prediction for latest data
  - `get_anomalies(repo_id, severity, limit)` — query anomaly history
  - Categorize: `pr_latency_spike`, `churn_surge`, `review_bottleneck`

**Afternoon — API + Scheduled Detection**
- [ ] Implement `GET /api/v1/anomalies?repo_id=&severity=&limit=`
- [ ] Add anomaly count to health check and dashboard summary
- [ ] Set up Cloud Scheduler to run detection hourly
- [ ] Test with injected anomalous data points

**Learning Focus:** Vertex AI deployment, batch vs online prediction, Cloud Scheduler

---

#### Day 12: Anomaly Dashboard
**Morning — Anomaly Feed**
- [ ] Build `useAnomalies.ts` hook
- [ ] Build `AnomalyTimeline.tsx`:
  - Timeline view with severity color coding (red/yellow/blue)
  - Each card: anomaly type, metric, expected vs actual, confidence %, timestamp
  - Click to jump to relevant chart with anomaly highlighted
- [ ] Build `Anomalies.tsx` page — filterable anomaly feed

**Afternoon — Dashboard Integration**
- [ ] Add anomaly overlay to metric charts (highlighted regions on PR latency, churn charts)
- [ ] Add anomaly badge count to sidebar navigation
- [ ] Build notification bell with recent anomalies dropdown
- [ ] Polish all loading/error/empty states

**Learning Focus:** Data visualization overlays, notification UI patterns, state management

---

### PHASE 5 — DEPLOYMENT & POLISH (Days 13–14)
**Goal:** Production-ready deployment, CI/CD, documentation.

#### Day 13: Containerization + CI/CD
**Morning — Docker + Cloud Run**
- [ ] Write `backend/Dockerfile` (multi-stage: build → slim runtime)
- [ ] Build and test image locally
- [ ] Push to Google Artifact Registry
- [ ] Deploy to Cloud Run:
  - Set env vars (GCP project, BigQuery dataset, Pub/Sub topics)
  - Configure min/max instances, memory, CPU
  - Set up custom domain (optional)
- [ ] Build frontend for production: `npm run build`
- [ ] Serve frontend via Cloud Run (bundle with backend) or Cloud Storage + CDN

**Afternoon — GitHub Actions**
- [ ] Build CI workflow (`.github/workflows/ci.yml`):
  - Trigger on PR to main
  - Steps: checkout → install → lint → type-check → unit tests → integration tests
- [ ] Build CD workflow (`.github/workflows/cd.yml`):
  - Trigger on merge to main
  - Steps: build Docker image → push to Artifact Registry → deploy to Cloud Run
- [ ] Add status badges to README

**Learning Focus:** Multi-stage Docker builds, Cloud Run deployment, GitHub Actions YAML

---

#### Day 14: Documentation + Final Polish
**Morning — Documentation**
- [ ] Write `docs/architecture.md` with system diagram (Mermaid)
- [ ] Write `docs/api-reference.md` (can auto-generate from FastAPI)
- [ ] Write `docs/setup-guide.md` — local dev + GCP setup step-by-step
- [ ] Write `docs/deployment.md` — Cloud Run deployment runbook
- [ ] Write Architecture Decision Records (ADRs) for key choices
- [ ] Polish `README.md` with badges, screenshots, architecture diagram

**Afternoon — Final Testing + Demo Prep**
- [ ] End-to-end test: onboard repo → data flows → metrics show → anomalies detect
- [ ] Cross-browser check dashboard
- [ ] Record a 2-minute demo video / GIF for README
- [ ] Create GitHub release with changelog
- [ ] Tag v1.0.0

**Learning Focus:** Technical writing, system documentation, release management

---

## 5. PROJECT MANAGEMENT SETUP

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

### Daily Dev Log Template
Keep a `DEV_LOG.md` at the project root:
```markdown
## Day X — YYYY-MM-DD

### Goals
- [ ] Goal 1
- [ ] Goal 2

### Completed
- What I built
- Key decisions made

### Blockers
- Issues encountered

### Learnings
- New concepts / techniques learned

### Tomorrow
- Plan for next session
```

---

## 6. KEY TECHNICAL CONCEPTS TO LEARN

### By Phase

**Phase 1 (Foundation):**
- FastAPI async patterns, dependency injection, middleware
- GitHub API (REST + pagination, rate limits)
- BigQuery SDK (schema definition, streaming inserts, parameterized queries)
- React project architecture (feature-based folder structure)

**Phase 2 (Metrics):**
- Analytical SQL (window functions, CTEs, PERCENTILE_CONT, DATE_TRUNC)
- Recharts/D3 for data visualization
- React Query (query keys, stale time, refetching, cache invalidation)
- API design patterns (filtering, pagination, response envelopes)

**Phase 3 (Real-Time):**
- Pub/Sub messaging (at-least-once delivery, ordering, dead-letter queues)
- Webhook security (HMAC signature verification)
- Apache Beam programming model (PCollections, windowing, triggers)
- Event-driven architecture patterns

**Phase 4 (ML):**
- Time-series feature engineering (lags, rolling stats, trends)
- Anomaly detection (Isolation Forest, Prophet, z-score methods)
- Vertex AI (training, deployment, prediction endpoints)
- ML pipeline orchestration

**Phase 5 (Deployment):**
- Docker multi-stage builds, image optimization
- Cloud Run (scaling, concurrency, cold starts)
- GitHub Actions (workflow syntax, secrets, artifacts)
- System documentation and ADRs

---

## 7. ENVIRONMENT VARIABLES (.env.example)

```env
# GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx
GITHUB_WEBHOOK_SECRET=your-webhook-secret
GITHUB_CLIENT_ID=your-oauth-client-id
GITHUB_CLIENT_SECRET=your-oauth-client-secret

# GCP
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=./service-account.json

# BigQuery
BQ_DATASET=devscope
BQ_LOCATION=US

# Pub/Sub
PUBSUB_TOPIC_EVENTS=github-events
PUBSUB_TOPIC_DLQ=github-events-dlq
PUBSUB_SUBSCRIPTION=github-events-sub

# Vertex AI
VERTEX_ENDPOINT_ID=your-endpoint-id
VERTEX_MODEL_ID=your-model-id

# App
API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5173
LOG_LEVEL=INFO
ENVIRONMENT=development
```

---

## 8. MAKEFILE REFERENCE

```makefile
.PHONY: dev test lint format setup

# Setup
setup:
	cd backend && pip install -r requirements.txt -r requirements-dev.txt
	cd frontend && npm install

# Development
dev-backend:
	cd backend && uvicorn app.main:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

dev:
	make -j2 dev-backend dev-frontend

# Testing
test-backend:
	cd backend && pytest -v --cov=app

test-frontend:
	cd frontend && npm run test

test:
	make test-backend && make test-frontend

# Quality
lint:
	cd backend && ruff check app/
	cd frontend && npm run lint

format:
	cd backend && ruff format app/
	cd frontend && npm run format

# Data
seed:
	cd backend && python scripts/seed_data.py

# Docker
build:
	docker build -t devscope-backend ./backend

run:
	docker run -p 8000:8000 --env-file .env devscope-backend
```

---

## 9. QUICK-START CHECKLIST (Do These Before Day 1)

- [ ] Create a GitHub repo: `devscope`
- [ ] Create a GCP project (free tier works for dev)
- [ ] Enable APIs: BigQuery, Pub/Sub, Cloud Run, Vertex AI, Artifact Registry
- [ ] Create a GCP service account with roles: BigQuery Admin, Pub/Sub Admin, Vertex AI User
- [ ] Download service account JSON key
- [ ] Generate a GitHub Personal Access Token (classic, `repo` + `read:org` scopes)
- [ ] Install local tools: Python 3.11+, Node 20+, Docker, gcloud CLI
- [ ] Set up `gcloud` CLI: `gcloud auth login && gcloud config set project YOUR_PROJECT_ID`
- [ ] Bookmark: [GitHub API docs](https://docs.github.com/en/rest), [BigQuery docs](https://cloud.google.com/bigquery/docs), [FastAPI docs](https://fastapi.tiangolo.com)
