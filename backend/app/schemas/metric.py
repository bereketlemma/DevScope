"""Metric Pydantic schemas."""
from pydantic import BaseModel


class MetricBase(BaseModel):
    """Base metric schema."""

    repository_id: int
    metric_name: str
    value: float


class DailyMetricResponse(BaseModel):
    """Daily metric response schema."""

    date: str
    metric_name: str
    value: float
    avg_value: float
    median_value: float
    p95_value: float


class RepositoryMetricsResponse(BaseModel):
    """Repository metrics response schema."""

    repository_id: int
    pr_latency_days: float | None = None
    pr_review_time_hours: float | None = None
    commit_frequency_daily: float | None = None
    pr_acceptance_rate: float | None = None
