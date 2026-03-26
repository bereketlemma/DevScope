"""
Vertex AI Training Job — Time-Series Anomaly Detection

Trains an Isolation Forest model on engineered features from BigQuery
daily metrics, then uploads the model to Vertex AI Model Registry.

Usage:
  python train.py --project YOUR_PROJECT --dataset devscope_dev --repo owner/repo
"""

from __future__ import annotations

import argparse
import logging
import pickle
from pathlib import Path

from google.cloud import aiplatform, storage
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

from preprocessing import fetch_training_data, build_features

logging.basicConfig(level=logging.INFO)
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

METRIC_TYPES = [
    "pr_merge_latency_median",
    "daily_code_churn",
    "review_turnaround_hours",
    "daily_pr_throughput",
]


def train_model(
    project_id: str,
    dataset: str,
    repo_id: str,
    region: str = "us-central1",
    contamination: float = 0.05,
) -> str:
    """
    Train an Isolation Forest on all metric types for a repository.

    Returns:
        GCS URI of the saved model artifact.
    """
    all_features = []

    for metric_name in METRIC_TYPES:
        logger.info("Fetching training data: %s / %s", repo_id, metric_name)
        raw_df = fetch_training_data(project_id, dataset, repo_id, metric_name)

        if len(raw_df) < 30:
            logger.warning(
                "Insufficient data for %s (%d rows), skipping", metric_name, len(raw_df)
            )
            continue

        features_df = build_features(raw_df)
        features_df["metric_type"] = metric_name
        all_features.append(features_df)

    if not all_features:
        raise ValueError(f"No sufficient training data for {repo_id}")

    import pandas as pd

    combined = pd.concat(all_features, ignore_index=True)
    X = combined[FEATURE_COLS].values

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train Isolation Forest
    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(X_scaled)

    # Evaluate on training data
    predictions = model.predict(X_scaled)
    anomaly_count = (predictions == -1).sum()
    logger.info(
        "Training complete: %d anomalies detected in %d samples (%.1f%%)",
        anomaly_count,
        len(X_scaled),
        anomaly_count / len(X_scaled) * 100,
    )

    # Save model artifacts locally
    artifact_dir = Path("/tmp/devscope_model")
    artifact_dir.mkdir(exist_ok=True)

    with open(artifact_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    with open(artifact_dir / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    # Upload to GCS
    bucket_name = f"{project_id}-devscope-models"
    gcs_uri = f"gs://{bucket_name}/anomaly-detection/latest/"

    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)

    for artifact_path in artifact_dir.iterdir():
        blob = bucket.blob(f"anomaly-detection/latest/{artifact_path.name}")
        blob.upload_from_filename(str(artifact_path))
        logger.info("Uploaded %s to %s", artifact_path.name, gcs_uri)

    # Register with Vertex AI
    aiplatform.init(project=project_id, location=region)
    model_resource = aiplatform.Model.upload(
        display_name="devscope-anomaly-detection",
        artifact_uri=gcs_uri,
        serving_container_image_uri="us-docker.pkg.dev/vertex-ai/prediction/sklearn-cpu.1-3:latest",
    )
    logger.info("Model registered: %s", model_resource.resource_name)

    return gcs_uri


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train DevScope anomaly model")
    parser.add_argument("--project", required=True, help="GCP project ID")
    parser.add_argument("--dataset", default="devscope_dev", help="BigQuery dataset")
    parser.add_argument("--repo", required=True, help="Repository (owner/repo)")
    parser.add_argument("--region", default="us-central1", help="GCP region")
    args = parser.parse_args()

    train_model(args.project, args.dataset, args.repo, args.region)
