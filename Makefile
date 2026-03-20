.PHONY: install dev format lint type-check test build up down logs

install:
	cd backend && pip install -e ".[dev]"
	cd frontend && npm install

dev:
	docker-compose up -d

format:
	cd backend && make format
	cd frontend && npm run format

lint:
	cd backend && make lint
	cd frontend && npm run lint

type-check:
	cd backend && make type-check
	cd frontend && npm run type-check

test:
	cd backend && make test

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-celery:
	docker-compose logs -f celery

db-migrate:
	docker-compose exec backend alembic upgrade head

db-downgrade:
	docker-compose exec backend alembic downgrade -1

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf backend/dist backend/build backend/*.egg-info
	rm -rf .ruff_cache .mypy_cache

help:
	@echo "DevScope Development Commands"
	@echo "=============================="
	@echo "make install       - Install dependencies"
	@echo "make dev           - Start development environment"
	@echo "make up            - Start Docker Compose"
	@echo "make down          - Stop Docker Compose"
	@echo "make logs          - View live logs"
	@echo "make format        - Format code"
	@echo "make lint          - Run linters"
	@echo "make type-check    - Type checking"
	@echo "make test          - Run tests"
	@echo "make build         - Build Docker images"
	@echo "make clean         - Clean build artifacts"
