"""Feature engineering for time-series anomaly detection."""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from google.cloud import bigquery

logger = logging.getLogger(__name__)


def build_features(metrics_df: pd.DataFrame) -> pd.DataFrame:
    """
    Engineer features from raw daily metrics for anomaly detection.

    Features:
      - lag_1, lag_7, lag_14: lagged metric values
      - rolling_mean_7, rolling_mean_14: rolling averages
      - rolling_std_7, rolling_std_14: rolling standard deviations
      - trend_7: slope of 7-day linear trend
      - day_of_week: cyclical feature
    """
    df = metrics_df.sort_values("metric_date").copy()

    # Lag features
    for lag in [1, 7, 14]:
        df[f"lag_{lag}"] = df["metric_value"].shift(lag)

    # Rolling statistics
    for window in [7, 14]:
        df[f"rolling_mean_{window}"] = (
            df["metric_value"].rolling(window=window, min_periods=1).mean()
        )
        df[f"rolling_std_{window}"] = (
            df["metric_value"].rolling(window=window, min_periods=1).std()
        )

    # Z-score relative to 14-day rolling window
    df["z_score_14"] = (
        (df["metric_value"] - df["rolling_mean_14"]) / df["rolling_std_14"]
    ).fillna(0)

    # 7-day trend (simple slope approximation)
    df["trend_7"] = df["metric_value"].diff(7) / 7

    # Day of week (cyclical)
    df["day_of_week"] = pd.to_datetime(df["metric_date"]).dt.dayofweek

    # Drop rows with NaN from lagging
    df = df.dropna().reset_index(drop=True)

    return df


def fetch_training_data(
    project_id: str,
    dataset: str,
    repo_id: str,
    metric_name: str,
    days: int = 180,
) -> pd.DataFrame:
    """Fetch daily metrics from BigQuery for model training."""
    client = bigquery.Client(project=project_id)

    query = f"""
        SELECT metric_date, metric_value
        FROM `{project_id}.{dataset}.daily_metrics`
        WHERE repo_id = @repo_id
          AND metric_name = @metric_name
          AND metric_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
        ORDER BY metric_date
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("repo_id", "STRING", repo_id),
            bigquery.ScalarQueryParameter("metric_name", "STRING", metric_name),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
    )

    return client.query(query, job_config=job_config).to_dataframe()
