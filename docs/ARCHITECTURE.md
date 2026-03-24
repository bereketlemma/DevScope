# DevScope Architecture

## System Overview

DevScope is a distributed engineering analytics platform built entirely on Google Cloud Platform. It mines GitHub repository data, streams it through a real-time pipeline, and surfaces productivity metrics through an interactive dashboard.

## Data Flow

```
GitHub API / Webhooks
        │
        ▼
┌─────────────────────┐
│  Ingestion Service   │  Cloud Run
│  (FastAPI)           │
│  - Fetches PRs,      │
│    commits, reviews  │
│  - Webhook receiver  │
│  - Rate-limit aware  │
└────────┬────────────┘
         │ publishes events
         ▼
┌─────────────────────┐
│  Google Cloud        │
│  Pub/Sub             │
│  - github-events     │
│  - github-events-dlq │
└────────┬────────────┘
         │ subscribes
         ▼
┌─────────────────────┐
│  Cloud Dataflow      │
│  (Apache Beam)       │
│  - Routes by type    │
│  - Transforms events │
│  - Validates schema  │
└────────┬────────────┘
         │ writes
         ▼
┌─────────────────────┐
│  BigQuery            │
│  - pull_requests     │  partitioned by date
│  - commits           │  clustered by repo_id
│  - reviews           │
│  - daily_metrics     │
└────────┬────────────┘
         │ queries
         ▼
┌─────────────────────┐
│  API Service         │  Cloud Run
│  (FastAPI)           │
│  - Metric queries    │
│  - Health scoring    │
│  - Anomaly detection │◀── Vertex AI
└────────┬────────────┘
         │ serves
         ▼
┌─────────────────────┐
│  React Dashboard     │
│  - PR Latency chart  │
│  - Code Churn chart  │
│  - Review Cycles     │
│  - Health Score gauge│
│  - Anomaly timeline  │
└─────────────────────┘
```

## Design Decisions

### BigQuery as sole data store (no PostgreSQL)
All data lives in BigQuery — both raw events and aggregated metrics. This eliminates the operational overhead of managing a relational database, leverages BigQuery's sub-second query performance on partitioned/clustered tables, and keeps the architecture purely GCP-native.

### Pub/Sub over Celery/Redis
Event streaming through Pub/Sub provides durable, at-least-once delivery with automatic dead-letter queuing. This replaces the need for Celery workers and a Redis broker, reducing infrastructure complexity.

### Vertex AI for anomaly detection
Time-series anomaly detection runs through Vertex AI with an Isolation Forest model. The system falls back to statistical z-score detection when Vertex AI is not configured, ensuring anomalies are always surfaced.

### Independent Cloud Run services
Each service (ingestion, API) deploys independently to Cloud Run, enabling independent scaling and deployment cycles.
