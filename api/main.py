"""
DevScope API Service — Cloud Run

Queries BigQuery analytics data and Vertex AI anomaly detection
to serve the React/TypeScript dashboard.

Endpoints:
  GET  /api/v1/metrics/repos                       — list tracked repos
  GET  /api/v1/metrics/{repo_id}/pr-latency        — PR merge latency
  GET  /api/v1/metrics/{repo_id}/code-churn         — code churn
  GET  /api/v1/metrics/{repo_id}/review-cycles      — review cycles
  GET  /api/v1/metrics/{repo_id}/health             — health score (0-100)
  GET  /api/v1/anomalies/{repo_id}                  — anomaly detection
  GET  /health                                       — liveness
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import config
from routes.metrics import router as metrics_router
from routes.anomalies import router as anomalies_router

logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("API service starting (env=%s)", config.environment)
    yield
    logger.info("API service stopped")


app = FastAPI(
    title="DevScope API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(metrics_router, prefix="/api/v1")
app.include_router(anomalies_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "api"}
