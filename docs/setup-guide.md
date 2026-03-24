# DevScope Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker Desktop
- Google Cloud SDK (`gcloud`)
- GitHub Personal Access Token (`repo` + `read:org` scopes)
- GCP account with billing enabled ($300 free trial)

## 1. Clone the Repository

```bash
git clone https://github.com/bereketlemma/devscope.git
cd devscope
```

## 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your values:
- `GCP_PROJECT_ID` — your GCP project
- `GITHUB_TOKEN` — personal access token
- `BQ_DATASET` — `devscope_dev` for development

## 3. Provision GCP Resources

```bash
chmod +x infra/setup_gcp.sh
./infra/setup_gcp.sh
```

This creates: BigQuery dataset + tables, Pub/Sub topics + subscriptions, GCS buckets, Artifact Registry, service account with roles.

## 4. Install Dependencies

```bash
make setup
```

## 5. Seed Sample Data

```bash
make seed
```

Generates 90 days of realistic PR, commit, review, and metric data in BigQuery.

## 6. Run Locally

```bash
make dev
```

This starts:
- **API** at http://localhost:8000 (FastAPI, queries BigQuery)
- **Ingestion** at http://localhost:8001 (FastAPI, publishes to Pub/Sub)
- **Frontend** at http://localhost:5173 (React dashboard)

## 7. Run Pipeline Locally

```bash
make pipeline-local
```

Uses Apache Beam's DirectRunner. For Cloud Dataflow deployment see `make pipeline-dataflow`.

## 8. Run Tests

```bash
make test
```

## Cost Estimates (GCP)

| Service         | Free Tier             | DevScope Usage    | Monthly Cost |
|----------------|-----------------------|-------------------|-------------|
| BigQuery        | 1TB queries, 10GB     | ~5-20GB queries   | $0          |
| Cloud Run       | 2M requests           | ~1K req/day       | $0          |
| Pub/Sub         | 10GB/month            | <1GB              | $0          |
| Dataflow        | None                  | ~$1-5/hr running  | $5-20       |
| Vertex AI       | $300 credit           | Training + predict| $10-30      |
| Storage         | 5GB                   | <1GB              | $0          |

**$300 free trial covers 10+ months of development.**
