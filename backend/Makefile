.PHONY: help install format lint test migrations run celery

help:
	@echo "DevScope Backend Commands"
	@echo "========================="
	@echo "make install      - Install dependencies"
	@echo "make format       - Format code with black and isort"
	@echo "make lint         - Run ruff linter"
	@echo "make type-check   - Run mypy type checker"
	@echo "make test         - Run pytest"
	@echo "make run          - Start development server"
	@echo "make celery       - Start Celery worker"
	@echo "make db-upgrade   - Run database migrations"

install:
	pip install -e ".[dev]"

format:
	black .
	isort .

lint:
	ruff check .

type-check:
	mypy .

test:
	pytest -v --cov=app tests/

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

celery:
	celery -A app.workers.celery_app worker --loglevel=info

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1
