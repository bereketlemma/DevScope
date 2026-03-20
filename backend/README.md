# DevScope Backend

Repository Intelligence Platform — Backend Service

## Features

- **FastAPI** REST API with async support
- **PostgreSQL** for application data (users, repos, sync jobs, anomalies)
- **BigQuery** for analytics and metrics
- **Celery** for background job processing
- **Redis** for caching and task queuing
- **GitHub OAuth2** authentication
- **JWT** token-based authorization
- **SQLAlchemy 2.0** with async ORM
- **Alembic** database migrations

## Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 16
- Redis 7
- GitHub OAuth application credentials
- GCP Project with BigQuery enabled

### Installation

```bash
cd backend
pip install -e ".[dev]"
```

### Configuration

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Database Setup

```bash
alembic upgrade head
```

## Running

### Development Server

```bash
make run
```

Server runs on `http://localhost:8000`

### Celery Worker

```bash
make celery
```

### Tests

```bash
make test
```

## API Endpoints

### Authentication

- `POST /api/v1/auth/login` — GitHub OAuth login
- `GET /api/v1/auth/me` — Get current user
- `POST /api/v1/auth/logout` — Logout

### Repositories

- `GET /api/v1/repositories` — List repositories
- `GET /api/v1/repositories/{repo_id}` — Get repository details
- `POST /api/v1/repositories/{repo_id}/sync` — Trigger repository sync

### Metrics

- `GET /api/v1/metrics/{repo_id}` — Get repository metrics
- `GET /api/v1/metrics/{repo_id}/daily` — Get daily metric history
- `GET /api/v1/metrics/{repo_id}/anomalies` — Get detected anomalies

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py
│   │   ├── repositories.py
│   │   └── metrics.py
│   ├── models/
│   │   ├── user.py
│   │   ├── repository.py
│   │   ├── sync_job.py
│   │   └── anomaly.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── repository.py
│   │   ├── metric.py
│   │   └── anomaly.py
│   ├── services/
│   │   ├── github_client.py
│   │   ├── bigquery_service.py
│   │   └── metrics_service.py
│   ├── workers/
│   │   ├── celery_app.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   └── main.py
├── alembic/
├── tests/
└── Dockerfile
```

## Development

### Format Code

```bash
make format
```

### Lint Code

```bash
make lint
```

### Type Checking

```bash
make type-check
```

## Docker

```bash
docker build -t devscope-backend .
docker run -p 8000:8000 devscope-backend
```

## License

MIT
