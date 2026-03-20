"""Anomaly Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AnomalyBase(BaseModel):
    """Base anomaly schema."""

    repository_id: int
    metric_name: str
    detected_value: float
    z_score: float
    threshold: float


class AnomalyResponse(AnomalyBase):
    """Anomaly response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str | None = None
    created_at: datetime
