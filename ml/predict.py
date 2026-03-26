"""
Batch and online prediction using trained Vertex AI models.

Can run standalone for batch scoring or be called from the API service.
"""

from __future__ import annotations

import logging
from typing import Any

from google.cloud import aiplatform

from preprocessing import fetch_training_data, build_features

logger = logging.getLogger(__name__)

FEATURE_COLS = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_mean_7",
    "rolling_mean_14",
    "rolling_std_7",
    "rolling_std_14",
    "z_score_14",
    "trend_7",
    "day_of_week",
]


def predict_anomalies(
    project_id: str,
    region: str,
    endpoint_id: str,
    dataset: str,
    repo_id: str,
    metric_name: str,
    days: int = 30,
) -> list[dict[str, Any]]:
    """
    Run anomaly prediction on recent metrics via Vertex AI endpoint.

    Returns list of detected anomalies with confidence scores.
    """
    aiplatform.init(project=project_id, location=region)
    endpoint = aiplatform.Endpoint(endpoint_id)

    # Fetch and engineer features
    raw_df = fetch_training_data(project_id, dataset, repo_id, metric_name, days + 14)
    if len(raw_df) < 14:
        logger.warning("Insufficient data for prediction (%d rows)", len(raw_df))
        return []

    features_df = build_features(raw_df)

    # Only predict on the most recent `days` worth of data
    recent = features_df.tail(days)
    instances = recent[FEATURE_COLS].values.tolist()

    # Call Vertex AI endpoint
    response = endpoint.predict(instances=instances)

    anomalies = []
    for i, (pred, row) in enumerate(zip(response.predictions, recent.itertuples())):
        # Isolation Forest returns -1 for anomalies
        is_anomaly = (
            pred == -1
            if isinstance(pred, (int, float))
            else pred.get("is_anomaly", False)
        )
        score = abs(row.z_score_14) / 5.0  # Normalize as confidence proxy

        if is_anomaly:
            anomalies.append(
                {
                    "metric_date": str(row.metric_date),
                    "metric_name": metric_name,
                    "metric_value": row.metric_value,
                    "expected_value": row.rolling_mean_14,
                    "z_score": row.z_score_14,
                    "confidence": min(score, 1.0),
                    "severity": _classify(score),
                }
            )

    logger.info(
        "Predicted %d anomalies for %s/%s", len(anomalies), repo_id, metric_name
    )
    return anomalies


def _classify(confidence: float) -> str:
    if confidence >= 0.95:
        return "CRITICAL"
    if confidence >= 0.85:
        return "HIGH"
    return "MEDIUM"
