"""Anomaly API routes — Vertex AI anomaly detection results."""

from __future__ import annotations

from fastapi import APIRouter, Query

from services.bigquery_service import BigQueryService
from services.anomaly_service import AnomalyService

router = APIRouter(prefix="/anomalies", tags=["anomalies"])

bq = BigQueryService()
anomaly_svc = AnomalyService(bq)


@router.get("/{repo_id:path}")
async def get_anomalies(
    repo_id: str,
    days: int = Query(default=30, ge=7, le=365),
    severity: str | None = Query(default=None, pattern="^(MEDIUM|HIGH|CRITICAL)$"),
):
    """
    Detect anomalies for a repository.

    Uses Vertex AI time-series detection when configured,
    falls back to z-score statistical detection.
    """
    anomalies = await anomaly_svc.detect_anomalies(repo_id, days)

    if severity:
        anomalies = [a for a in anomalies if a["severity"] == severity]

    return {
        "data": anomalies,
        "meta": {
            "repo_id": repo_id,
            "window_days": days,
            "total": len(anomalies),
            "detection_method": "vertex_ai" if anomaly_svc._vertex_enabled else "z_score",
        },
    }
