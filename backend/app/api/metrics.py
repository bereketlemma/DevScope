"""Metrics endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.metric import DailyMetricResponse, RepositoryMetricsResponse

router = APIRouter()


@router.get("/{repo_id}", response_model=RepositoryMetricsResponse)
async def get_repository_metrics(
    repo_id: int, session: AsyncSession = Depends(get_session)
) -> dict:
    """Get repository metrics snapshot."""
    # TODO: Query BigQuery for aggregated metrics
    raise HTTPException(status_code=404, detail="Repository not found")


@router.get("/{repo_id}/daily", response_model=list[DailyMetricResponse])
async def get_daily_metrics(
    repo_id: int,
    days: int = 30,
    session: AsyncSession = Depends(get_session),
) -> list:
    """Get daily metric history."""
    # TODO: Query BigQuery for time-series data
    return []


@router.get("/{repo_id}/anomalies")
async def get_repository_anomalies(
    repo_id: int, session: AsyncSession = Depends(get_session)
) -> dict:
    """Get detected anomalies for repository."""
    # TODO: Fetch recent anomalies from PostgreSQL
    return {"anomalies": []}
