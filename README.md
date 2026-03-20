# DevScope — Repository Intelligence Platform

![CI](https://github.com/yourusername/devscope/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![Node](https://img.shields.io/badge/node-20-blue.svg)

A distributed engineering productivity platform that mines GitHub repositories via the GitHub API, correlates developer metrics (PR latency, code churn, review cycles), aggregates data into BigQuery, and uses statistical anomaly detection to surface insights in a React dashboard.

## 🎯 Features

- **GitHub Integration**: OAuth2 authentication, automated repo sync via GitHub API
- **Metrics Tracking**: PR latency, review cycles, commit frequency, code churn
- **Anomaly Detection**: Z-score based statistical detection ($ |z| > 3 $)
- **Real-time Dashboard**: React 18 + Recharts for metrics visualization
- **Scalable Backend**: FastAPI + PostgreSQL + BigQuery + Redis
- **Background Jobs**: Celery workers for async GitHub syncs
- **Production Ready**: Docker Compose, GitHub Actions CI/CD, CodeQL security analysis

## 📊 Architecture

```
GitHub API ──► FastAPI Backend ──► PostgreSQL (app data)
                    │                  │
                    ├──► Celery ──► BigQuery (analytics)
                    │
                    └──► React Dashboard
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture.

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose
- GitHub OAuth app credentials
- GCP Project (with BigQuery enabled)

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/devscope.git
cd devscope

# 2. Create .env
cat > .env << EOF
DEBUG=True
ENV=dev
DATABASE_URL=postgresql+asyncpg://devscope:devscope@localhost:5432/devscope
REDIS_URL=redis://localhost:6379
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
SECRET_KEY=dev-secret-key
GCP_PROJECT_ID=your_gcp_project
BQ_DATASET_ID=devscope
EOF

# 3. Start services
make dev

# 4. Open browser
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Available Commands

```bash
make install       # Install dependencies
make dev           # Start Docker Compose
make up            # Start Docker services
make down          # Stop Docker services
make format        # Format code
make lint          # Lint code
make type-check    # Type checking
make test          # Run tests
make logs          # View live logs
make clean         # Clean build artifacts
```

## 📁 Project Structure

```
devscope/
├── backend/
│   ├── app/
│   │   ├── api/           # Route handlers
│   │   ├── models/        # SQLAlchemy ORM
│   │   ├── schemas/       # Pydantic validation
│   │   ├── services/      # Business logic
│   │   ├── workers/       # Celery tasks
│   │   ├── core/          # Config, DB, security
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   ├── tests/             # Unit tests
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── Makefile
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Route pages
│   │   ├── services/      # API client
│   │   ├── hooks/         # Zustand stores
│   │   ├── types/         # TypeScript interfaces
│   │   └── App.tsx
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DATA_MODEL.md
│   └── ADR.md
├── .github/
│   ├── workflows/         # GitHub Actions
│   └── ISSUE_TEMPLATE/    # Issue templates
├── docker-compose.yml
├── Makefile
└── README.md
```

## 🔧 Tech Stack

### Backend
- **Framework**: FastAPI 0.104
- **Database**: PostgreSQL 16 + SQLAlchemy 2.0 + Alembic
- **Analytics**: Google BigQuery
- **Task Queue**: Celery 5.3 + Redis 7
- **Authentication**: GitHub OAuth2 + JWT
- **Server**: Uvicorn + Gunicorn

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite 5
- **Styling**: Tailwind CSS 3.3
- **Charts**: Recharts 2.10
- **State Management**: Zustand 4.4
- **HTTP Client**: Axios 1.6

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **CI/CD**: GitHub Actions
- **Code Quality**: Ruff, Black, ESLint, Prettier
- **Security**: CodeQL, Dependabot
- **Hosting**: Google Cloud Run (M2)

## 📚 Documentation

- [Architecture Decision Records](docs/ADR.md)
- [API Reference](docs/API.md)
- [Data Model](docs/DATA_MODEL.md)
- [Complete Architecture](docs/ARCHITECTURE.md)

## 🔐 Security

- GitHub OAuth2 for authentication
- JWT tokens (HS256) stored in localStorage
- CORS middleware for frontend protection
- Input validation with Pydantic
- Parameterized queries to prevent SQL injection
- Environment variables for secrets
- CodeQL security scanning in CI

## 📊 Metrics Tracked

- **PR Latency**: Avg days from creation to merge
- **Review Cycle**: Avg hours from creation to first review
- **Commit Frequency**: Commits per day
- **PR Acceptance Rate**: Merged / total PRs
- **Code Churn**: Additions + deletions per commit

## 🚨 Anomaly Detection

Uses Z-score method: $ z = \frac{x - \mu}{\sigma} $

Flags triggered when $ |z| > 3 $ (99.7% confidence interval).

Example: PR latency of 10 days (when avg is 2 ± 0.5) triggers an anomaly.

## 🧪 Testing

```bash
# Backend tests
cd backend
make test

# Frontend type checking
cd frontend
npm run type-check
```

## 📦 Deployment

### Docker Compose (Local/Dev)

```bash
docker-compose up -d
```

### Google Cloud Run (Production - M2)

```bash
# Build and push images
docker build -t gcr.io/YOUR_PROJECT/devscope-backend:latest ./backend
docker build -t gcr.io/YOUR_PROJECT/devscope-frontend:latest ./frontend
docker push gcr.io/YOUR_PROJECT/devscope-backend:latest
docker push gcr.io/YOUR_PROJECT/devscope-frontend:latest

# Deploy
gcloud run deploy devscope-backend --image gcr.io/YOUR_PROJECT/devscope-backend:latest
gcloud run deploy devscope-frontend --image gcr.io/YOUR_PROJECT/devscope-frontend:latest
```

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit: `git commit -m "feat: your feature"`
4. Lint & test: `make lint && make test`
5. Push and open PR

## 📋 Roadmap

### Milestone 1 (Weeks 1–4) ✅ In Progress
- [x] Backend scaffolding (FastAPI, SQLAlchemy, Celery)
- [x] Frontend dashboard (React 18, Tailwind)
- [x] GitHub OAuth integration
- [x] PostgreSQL + BigQuery setup
- [x] Metrics computation & anomaly detection
- [x] Docker & GitHub Actions CI/CD
- [ ] Deploy to Cloud Run
- [ ] Accessibility audit

### Milestone 2 (Weeks 5–6) 📅 Planned
- [ ] GitHub Webhooks → Pub/Sub → Dataflow
- [ ] Vertex AI anomaly detection
- [ ] Real-time metrics streaming
- [ ] Advanced filtering & exports

## 📄 License

MIT — see [LICENSE](LICENSE)

## 👥 Team

Built with ❤️ by the DevScope team.

---

**Questions?** Open an issue or check the [docs](docs/).
