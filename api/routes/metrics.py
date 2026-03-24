"""Metrics API routes — PR latency, code churn, review cycles, health score."""

from __future__ import annotations

from fastapi import APIRouter, Query

from services.bigquery_service import BigQueryService
from services.metrics_service import MetricsService

router = APIRouter(prefix="/metrics", tags=["metrics"])

bq = BigQueryService()
metrics_svc = MetricsService(bq)


@router.get("/repos")
async def list_repos():
    """List all repositories with ingested data."""
    repos = await bq.get_repos()
    return {"data": repos}


@router.get("/{repo_id:path}/pr-latency")
async def pr_latency(repo_id: str, days: int = Query(default=30, ge=7, le=365)):
    """PR merge latency — median and p95 hours to merge, grouped by day."""
    data = await bq.get_pr_latency(repo_id, days)
    return {"data": data, "meta": {"repo_id": repo_id, "window_days": days}}


@router.get("/{repo_id:path}/code-churn")
async def code_churn(repo_id: str, days: int = Query(default=30, ge=7, le=365)):
    """Code churn — additions, deletions, net churn by day."""
    data = await bq.get_code_churn(repo_id, days)
    return {"data": data, "meta": {"repo_id": repo_id, "window_days": days}}


@router.get("/{repo_id:path}/review-cycles")
async def review_cycles(repo_id: str, days: int = Query(default=30, ge=7, le=365)):
    """Review cycles — rounds per PR, time to first review."""
    data = await bq.get_review_cycles(repo_id, days)
    return {"data": data, "meta": {"repo_id": repo_id, "window_days": days}}


@router.get("/{repo_id:path}/health")
async def health_score(repo_id: str, days: int = Query(default=30, ge=7, le=365)):
    """Composite health score (0–100) with breakdown."""
    data = await metrics_svc.get_health_score(repo_id, days)
    return {"data": data}
