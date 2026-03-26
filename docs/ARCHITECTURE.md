# DevScope Architecture — v1.0

## System overview

DevScope is a distributed engineering analytics platform built on Google Cloud Platform. It mines GitHub repository data through a streaming pipeline and surfaces productivity metrics through an interactive dashboard.

## Architecture diagram

![DevScope Architecture](devscope-architecture.png)

## Data flow

```
GitHub API / Webhooks
        │
        ▼
┌─────────────────────┐
│  Ingestion service   │  Cloud Run (port 8001)
│  Python + FastAPI    │
│  • Fetch PRs,        │
│    commits, reviews  │
│  • Webhook receiver  │
│  • Rate-limit aware  │
└────────┬────────────┘
         │ publishes JSON events
         ▼
┌─────────────────────┐
│  Cloud Pub/Sub       │
│  • github-events     │
│  • github-events-dlq │
│  • github-events-sub │
└────────┬────────────┘
         │ subscribes
         ▼
┌─────────────────────┐
│  Cloud Dataflow      │
│  Apache Beam         │
│  • Route by type     │
│  • Transform payload │
│  • Validate schema   │
│  • Write to BigQuery │
└────────┬────────────┘
         │ streaming inserts
         ▼
┌─────────────────────┐
│  BigQuery            │
│  4 tables            │
│  Partitioned by date │
│  Clustered by repo   │
└────────┬────────────┘
         │ parameterized queries
         ▼
┌─────────────────────┐
│  API service         │  Cloud Run (port 8000)
│  Python + FastAPI    │
│  • Query metrics     │
│  • Health scoring    │
│  • Anomaly detection │◀── Vertex AI (Isolation Forest)
└────────┬────────────┘
         │ JSON responses
         ▼
┌─────────────────────┐
│  React dashboard     │  Cloud Run (port 8080)
│  TypeScript + Vite   │
│  • Health gauge      │
│  • PR latency chart  │
│  • Code churn bars   │
│  • Review cycles     │
│  • Anomaly feed      │
└─────────────────────┘
```

## BigQuery schema

All tables live in the `devscope_dev` dataset (production: `devscope_prod`).

### pull_requests

Partitioned by `created_date`, clustered by `repo_id`.

| Column | Type | Description |
|---|---|---|
| pr_id | STRING | GitHub PR ID (primary key) |
| repo_id | STRING | Repository full name (owner/repo) |
| number | INTEGER | PR number |
| title | STRING | PR title |
| author | STRING | GitHub username of author |
| state | STRING | open, closed, merged |
| created_at | TIMESTAMP | When PR was opened |
| first_review_at | TIMESTAMP | When first review was submitted |
| approved_at | TIMESTAMP | When PR was approved |
| merged_at | TIMESTAMP | When PR was merged |
| closed_at | TIMESTAMP | When PR was closed |
| additions | INTEGER | Lines added |
| deletions | INTEGER | Lines deleted |
| changed_files | INTEGER | Number of files changed |
| review_rounds | INTEGER | Number of review rounds |
| created_date | DATE | Partition column |

### commits

Partitioned by `committed_date`, clustered by `repo_id`.

| Column | Type | Description |
|---|---|---|
| commit_sha | STRING | Git commit SHA (primary key) |
| repo_id | STRING | Repository full name |
| author | STRING | GitHub username |
| message | STRING | Commit message |
| committed_at | TIMESTAMP | When commit was made |
| additions | INTEGER | Lines added |
| deletions | INTEGER | Lines deleted |
| committed_date | DATE | Partition column |

### reviews

Clustered by `repo_id`.

| Column | Type | Description |
|---|---|---|
| review_id | STRING | GitHub review ID (primary key) |
| pr_id | STRING | Associated PR ID (foreign key) |
| repo_id | STRING | Repository full name |
| reviewer | STRING | GitHub username of reviewer |
| state | STRING | APPROVED, CHANGES_REQUESTED, COMMENTED |
| submitted_at | TIMESTAMP | When review was submitted |

### daily_metrics

Partitioned by `metric_date`, clustered by `repo_id`.

| Column | Type | Description |
|---|---|---|
| repo_id | STRING | Repository full name |
| metric_date | DATE | Date of measurement (partition column) |
| metric_name | STRING | pr_merge_latency_median, daily_code_churn, review_turnaround_hours, daily_pr_throughput |
| metric_value | FLOAT | Metric value |
| developer | STRING | Developer username (NULL = repo-level aggregate) |

### Table relationships

```
pull_requests ──┐
                ├──▶ daily_metrics (aggregated)
commits ────────┘
        │
        └── reviews (1:many via pr_id)
```

## API endpoints

| Method | Path | Description |
|---|---|---|
| GET | /api/v1/metrics/repos | List tracked repositories |
| GET | /api/v1/metrics/{repo_id}/pr-latency | PR merge latency (median + p95) |
| GET | /api/v1/metrics/{repo_id}/code-churn | Code churn by date |
| GET | /api/v1/metrics/{repo_id}/review-cycles | Review rounds and turnaround |
| GET | /api/v1/metrics/{repo_id}/health | Health score (0–100) with breakdown |
| GET | /api/v1/anomalies/{repo_id} | Anomaly detection results |
| POST | /ingest/{owner}/{repo} | Trigger historical backfill |
| POST | /sync/{owner}/{repo} | Incremental sync (last 24h) |
| POST | /webhooks/github | Real-time webhook receiver |
| GET | /health | Liveness check |

## Anomaly detection

### Z-score detection (v1 — active)

Statistical detection using 14-day rolling windows:
- Compute rolling mean and standard deviation
- Flag values exceeding 2σ from the mean
- Severity: MEDIUM (>2σ), HIGH (>3σ), CRITICAL (>4σ)
- Types: latency_spike, churn_surge, review_bottleneck, throughput_drop

### Vertex AI detection (v1 — trained, not deployed as endpoint)

Isolation Forest model trained on engineered features:
- Lag features: 1-day, 7-day, 14-day
- Rolling statistics: 7-day and 14-day mean and standard deviation
- Z-score relative to 14-day window
- 7-day trend (slope approximation)
- Day-of-week cyclical feature
- Training result: 16 anomalies in 304 samples (5.3% contamination)

## Health score computation

Weighted composite score (0–100):

| Component | Weight | Calculation |
|---|---|---|
| PR latency | 30% | Penalizes median merge time above 24 hours |
| Code churn stability | 20% | Lower variance in daily churn = higher score |
| Review coverage | 30% | Percentage of PRs with at least one review |
| Deployment frequency | 20% | Daily merge rate (target: 1+ per day) |

## Deployment

| Service | Platform | Port | Image |
|---|---|---|---|
| Frontend | Cloud Run | 8080 | devscope/frontend |
| API | Cloud Run | 8000 | devscope/api |
| Ingestion | Cloud Run | 8001 | devscope/ingestion |

All images built via Cloud Build and stored in Artifact Registry (`us-central1-docker.pkg.dev/devscope-491221/devscope/`).

## Cost profile (GCP free tier)

| Service | Monthly cost |
|---|---|
| BigQuery | $0 (under 1TB free queries) |
| Cloud Run | $0 (under 2M free requests) |
| Pub/Sub | $0 (under 10GB free) |
| Vertex AI | $0 (model registered, no active endpoint) |
| Cloud Build | $0 (120 free build-minutes/day) |
| Storage | $0 (under 5GB free) |
| **Total** | **$0** |
