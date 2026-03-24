.PHONY: dev test lint setup seed deploy

# ─── Setup ─────────────────────────────────────────
setup:
	cd ingestion && pip install -r requirements.txt
	cd pipeline && pip install -r requirements.txt
	cd api && pip install -r requirements.txt
	cd ml && pip install -r requirements.txt
	cd frontend && npm ci

# ─── GCP Infrastructure ───────────────────────────
infra-setup:
	chmod +x infra/setup_gcp.sh
	./infra/setup_gcp.sh

# ─── Development ───────────────────────────────────
dev-api:
	cd api && uvicorn main:app --reload --port 8000

dev-ingestion:
	cd ingestion && uvicorn main:app --reload --port 8001

dev-frontend:
	cd frontend && npm run dev

dev:
	make -j3 dev-api dev-ingestion dev-frontend

# ─── Pipeline (local) ─────────────────────────────
pipeline-local:
	cd pipeline && python main.py --runner DirectRunner

pipeline-dataflow:
	cd pipeline && python main.py \
		--runner DataflowRunner \
		--project $(GCP_PROJECT_ID) \
		--region $(GCP_REGION) \
		--temp_location gs://$(GCP_PROJECT_ID)-dataflow-temp/tmp

# ─── Testing ───────────────────────────────────────
test-ingestion:
	cd tests && pytest ingestion/ -v

test-pipeline:
	cd tests && pytest pipeline/ -v

test-api:
	cd tests && pytest api/ -v

test-ml:
	cd tests && pytest ml/ -v

test-frontend:
	cd frontend && npm run test

test:
	make test-ingestion test-pipeline test-api test-ml

# ─── Quality ───────────────────────────────────────
lint:
	ruff check ingestion/ api/ pipeline/ ml/
	cd frontend && npm run lint

format:
	ruff format ingestion/ api/ pipeline/ ml/
	cd frontend && npx prettier --write src/

# ─── Data ──────────────────────────────────────────
seed:
	python scripts/seed_bigquery.py

# ─── Docker ────────────────────────────────────────
build-ingestion:
	docker build -t devscope-ingestion ./ingestion

build-api:
	docker build -t devscope-api ./api

build-pipeline:
	docker build -t devscope-pipeline ./pipeline

build: build-ingestion build-api build-pipeline

# ─── Deploy ────────────────────────────────────────
deploy:
	chmod +x scripts/deploy.sh
	./scripts/deploy.sh
