# Contributing to DevScope

Thanks for your interest in contributing to DevScope! This guide will help you get started.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/bereketlemma/DevScope.git
cd DevScope
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your GCP project ID and GitHub token
```

3. Install dependencies:
```bash
# Backend
pip install -r api/requirements.txt
pip install -r ingestion/requirements.txt
pip install -r ml/requirements.txt

# Frontend
cd frontend && npm ci
```

4. Run locally:
```bash
# Terminal 1 — API
cd api && python -m uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

## Running Tests

```bash
# Set PYTHONPATH
export PYTHONPATH=api:ingestion:pipeline:ml  # Linux/Mac
$env:PYTHONPATH = "api;ingestion;pipeline;ml"  # Windows PowerShell

# Run tests
pytest tests/ -v --ignore=tests/pipeline
```

## Code Quality

We use `ruff` for Python linting/formatting and `eslint`/`prettier` for TypeScript:

```bash
# Python
ruff check ingestion/ api/ pipeline/ ml/ --fix
ruff format ingestion/ api/ pipeline/ ml/

# Frontend
cd frontend && npm run lint
cd frontend && npx tsc --noEmit
```

## Pull Request Process

1. Create a feature branch: `git checkout -b feat/your-feature`
2. Make your changes
3. Run tests and lint locally
4. Push and open a PR against `main`
5. CI must pass (lint, tests, type-check) before merge

## Commit Convention

We use conventional commits:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation
- `style:` — formatting, lint fixes
- `refactor:` — code restructuring
- `test:` — adding tests
- `chore:` — maintenance tasks
- `ci:` — CI/CD changes

## Project Architecture

```
ingestion/  → GitHub API → Pub/Sub (Cloud Run)
pipeline/   → Pub/Sub → Dataflow → BigQuery (Apache Beam)
api/        → BigQuery → FastAPI → Dashboard (Cloud Run)
ml/         → BigQuery → Vertex AI (Isolation Forest)
frontend/   → React/TypeScript dashboard (Cloud Run)
```

## Questions?

Open an issue or reach out via the repository discussions.
