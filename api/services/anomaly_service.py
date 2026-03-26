"""Anomaly detection service — Vertex AI time-series anomaly detection."""

from __future__ import annotations

import logging
from typing import Any

from google.cloud import aiplatform

from config import config
from services.bigquery_service import BigQueryService

logger = logging.getLogger(__name__)


class AnomalyService:
    """Detects productivity regressions using Vertex AI and z-score fallback."""

    def __init__(self, bq: BigQueryService) -> None:
        self._bq = bq
        self._vertex_enabled = bool(config.vertex_endpoint_id)

        if self._vertex_enabled:
            aiplatform.init(
                project=config.gcp_project_id,
                location=config.gcp_region,
            )
            self._endpoint = aiplatform.Endpoint(config.vertex_endpoint_id)

    async def detect_anomalies(
        self, repo_id: str, days: int = 30
    ) -> list[dict[str, Any]]:
        """
        Run anomaly detection on recent metrics.

        Uses Vertex AI endpoint if configured, otherwise falls back
        to z-score statistical detection.
        """
        if self._vertex_enabled:
            return await self._detect_vertex(repo_id, days)
        return await self._detect_zscore(repo_id, days)

    async def _detect_vertex(self, repo_id: str, days: int) -> list[dict[str, Any]]:
        """Vertex AI time-series anomaly detection."""
        # Fetch recent daily metrics for all metric types
        metrics = await self._bq.get_daily_metrics(
            repo_id, "pr_merge_latency_median", days
        )
        if not metrics:
            return []

        # Prepare instances for prediction
        instances = [
            {
                "metric_date": str(m["metric_date"]),
                "metric_value": float(m["metric_value"] or 0),
            }
            for m in metrics
        ]

        try:
            predictions = self._endpoint.predict(instances=instances)
            anomalies = []
            for i, pred in enumerate(predictions.predictions):
                is_anomaly = pred.get("is_anomaly", False)
                confidence = pred.get("confidence", 0.0)

                if is_anomaly and confidence >= 0.8:
                    anomalies.append(
                        {
                            "repo_id": repo_id,
                            "metric_date": instances[i]["metric_date"],
                            "metric_name": "pr_merge_latency_median",
                            "metric_value": instances[i]["metric_value"],
                            "expected_value": pred.get("expected_value"),
                            "confidence": confidence,
                            "severity": self._classify_severity(confidence),
                            "anomaly_type": "latency_spike",
                        }
                    )

            return anomalies

        except Exception as e:
            logger.error("Vertex AI prediction failed, falling back to z-score: %s", e)
            return await self._detect_zscore(repo_id, days)

    async def _detect_zscore(self, repo_id: str, days: int) -> list[dict[str, Any]]:
        """
        Statistical z-score anomaly detection.

        Flags values >2σ from 14-day rolling mean.
        Severity: >2σ MEDIUM, >3σ HIGH, >4σ CRITICAL
        """
        metric_types = [
            ("pr_merge_latency_median", "latency_spike"),
            ("daily_code_churn", "churn_surge"),
            ("review_turnaround_hours", "review_bottleneck"),
            ("daily_pr_throughput", "throughput_drop"),
        ]

        all_anomalies = []

        for metric_name, anomaly_type in metric_types:
            metrics = await self._bq.get_daily_metrics(repo_id, metric_name, days)
            if len(metrics) < 14:
                continue

            values = [float(m["metric_value"] or 0) for m in metrics]

            # 14-day rolling window z-score
            for i in range(14, len(values)):
                window = values[i - 14 : i]
                mean = sum(window) / len(window)
                variance = sum((v - mean) ** 2 for v in window) / len(window)
                std = variance**0.5

                if std == 0:
                    continue

                z_score = abs(values[i] - mean) / std

                if z_score > 2.0:
                    severity = self._classify_severity_zscore(z_score)
                    all_anomalies.append(
                        {
                            "repo_id": repo_id,
                            "metric_date": str(metrics[i]["metric_date"]),
                            "metric_name": metric_name,
                            "metric_value": values[i],
                            "expected_value": round(mean, 2),
                            "z_score": round(z_score, 2),
                            "confidence": min(z_score / 5.0, 1.0),
                            "severity": severity,
                            "anomaly_type": anomaly_type,
                        }
                    )

        return sorted(all_anomalies, key=lambda a: a["metric_date"], reverse=True)

    @staticmethod
    def _classify_severity(confidence: float) -> str:
        if confidence >= 0.95:
            return "CRITICAL"
        if confidence >= 0.90:
            return "HIGH"
        return "MEDIUM"

    @staticmethod
    def _classify_severity_zscore(z_score: float) -> str:
        if z_score >= 4.0:
            return "CRITICAL"
        if z_score >= 3.0:
            return "HIGH"
        return "MEDIUM"
