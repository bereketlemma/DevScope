"""Metrics computation service."""
import logging
from typing import Any

import numpy as np

logger = logging.getLogger(__name__)


class MetricsService:
    """Service for computing metrics and anomalies."""

    Z_SCORE_THRESHOLD = 3.0

    @staticmethod
    def detect_anomalies(values: list[float], metric_name: str) -> list[dict[str, Any]]:
        """Detect anomalies using Z-score method."""
        if len(values) < 2:
            return []

        arr = np.array(values)
        mean = np.mean(arr)
        std = np.std(arr)

        if std == 0:
            return []

        anomalies = []
        for value in values:
            z_score = abs((value - mean) / std)
            if z_score > MetricsService.Z_SCORE_THRESHOLD:
                anomalies.append(
                    {
                        "metric_name": metric_name,
                        "detected_value": float(value),
                        "z_score": float(z_score),
                        "threshold": MetricsService.Z_SCORE_THRESHOLD,
                    }
                )

        return anomalies

    @staticmethod
    def calculate_pr_latency(pr_data: list[dict[str, Any]]) -> float:
        """Calculate average PR latency in days."""
        if not pr_data:
            return 0.0

        latencies = [
            (pr["closed_at"] - pr["created_at"]).days
            for pr in pr_data
            if pr.get("closed_at")
        ]

        return sum(latencies) / len(latencies) if latencies else 0.0

    @staticmethod
    def calculate_commit_frequency(commits: list[dict[str, Any]], days: int = 30) -> float:
        """Calculate daily commit frequency."""
        if not commits:
            return 0.0
        return len(commits) / days
