"""BigQuery analytics service."""
import logging
from typing import Any

from google.cloud import bigquery

from app.core.config import settings

logger = logging.getLogger(__name__)


class BigQueryService:
    """BigQuery analytics service."""

    def __init__(self) -> None:
        """Initialize BigQuery service."""
        self.client = bigquery.Client(project=settings.GCP_PROJECT_ID)
        self.dataset_id = settings.BQ_DATASET_ID

    def insert_pull_requests(self, rows: list[dict[str, Any]]) -> None:
        """Insert pull request events."""
        table_id = f"{settings.GCP_PROJECT_ID}.{self.dataset_id}.pull_requests"
        errors = self.client.insert_rows_json(table_id, rows)
        if errors:
            logger.error(f"Errors inserting to BigQuery: {errors}")

    def insert_commits(self, rows: list[dict[str, Any]]) -> None:
        """Insert commit events."""
        table_id = f"{settings.GCP_PROJECT_ID}.{self.dataset_id}.commits"
        errors = self.client.insert_rows_json(table_id, rows)
        if errors:
            logger.error(f"Errors inserting to BigQuery: {errors}")

    def get_repository_metrics(self, repo_id: int) -> dict[str, Any]:
        """Get aggregated metrics for repository."""
        query = f"""
        SELECT
            ROUND(AVG(TIMESTAMP_DIFF(closed_at, created_at, HOUR) / 24.0), 2) as pr_latency_days,
            ROUND(AVG(TIMESTAMP_DIFF(closed_at, created_at, MINUTE)), 2) as review_time_minutes,
            COUNT(*) / 30 as daily_velocity
        FROM `{settings.GCP_PROJECT_ID}.{self.dataset_id}.pull_requests`
        WHERE repository_id = @repo_id
        AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("repo_id", "INTEGER", repo_id)]
        )
        result = self.client.query(query, job_config=job_config)
        rows = list(result)
        if rows:
            return dict(rows[0])
        return {}

    def get_daily_metrics(self, repo_id: int, days: int = 30) -> list[dict[str, Any]]:
        """Get daily metric history."""
        query = f"""
        SELECT
            DATE(created_at) as date,
            COUNT(*) as pr_count,
            AVG(TIMESTAMP_DIFF(closed_at, created_at, HOUR)) as avg_review_hours
        FROM `{settings.GCP_PROJECT_ID}.{self.dataset_id}.pull_requests`
        WHERE repository_id = @repo_id
        AND created_at >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL @days DAY)
        GROUP BY date
        ORDER BY date DESC
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("repo_id", "INTEGER", repo_id),
                bigquery.ScalarQueryParameter("days", "INTEGER", days),
            ]
        )
        result = self.client.query(query, job_config=job_config)
        return [dict(row) for row in result]
