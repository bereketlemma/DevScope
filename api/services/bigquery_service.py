"""BigQuery service — reads analytics data for the API."""

from __future__ import annotations

import logging
from typing import Any

from google.cloud import bigquery

from config import config

logger = logging.getLogger(__name__)


class BigQueryService:
    """Executes parameterized queries against BigQuery analytics tables."""

    def __init__(self) -> None:
        self._client = bigquery.Client(
            project=config.gcp_project_id,
            location=config.bq_location,
        )
        self._dataset = config.bq_dataset

    def _table(self, name: str) -> str:
        return f"`{config.gcp_project_id}.{self._dataset}.{name}`"

    async def query(self, sql: str, params: list | None = None) -> list[dict[str, Any]]:
        """Execute a parameterized query and return rows as dicts."""
        job_config = bigquery.QueryJobConfig()
        if params:
            job_config.query_parameters = params

        query_job = self._client.query(sql, job_config=job_config)
        results = query_job.result()
        return [dict(row) for row in results]

    async def get_repos(self) -> list[dict[str, Any]]:
        """Get distinct repositories from ingested data."""
        sql = f"""
            SELECT DISTINCT repo_id, COUNT(*) as pr_count
            FROM {self._table('pull_requests')}
            GROUP BY repo_id
            ORDER BY pr_count DESC
        """
        return await self.query(sql)

    async def get_pr_latency(
        self, repo_id: str, days: int = 30
    ) -> list[dict[str, Any]]:
        """PR latency metrics — time to first review, approval, merge."""
        sql = f"""
            SELECT
                created_date,
                APPROX_QUANTILES(
                    TIMESTAMP_DIFF(merged_at, created_at, HOUR), 100
                )[OFFSET(50)] AS median_hours_to_merge,
                APPROX_QUANTILES(
                    TIMESTAMP_DIFF(merged_at, created_at, HOUR), 100
                )[OFFSET(95)] AS p95_hours_to_merge,
                COUNT(*) AS pr_count
            FROM {self._table('pull_requests')}
            WHERE repo_id = @repo_id
              AND merged_at IS NOT NULL
              AND created_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
            GROUP BY created_date
            ORDER BY created_date
        """
        params = [
            bigquery.ScalarQueryParameter("repo_id", "STRING", repo_id),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
        return await self.query(sql, params)

    async def get_code_churn(
        self, repo_id: str, days: int = 30
    ) -> list[dict[str, Any]]:
        """Code churn — additions, deletions, net churn by date."""
        sql = f"""
            SELECT
                committed_date,
                SUM(additions) AS total_additions,
                SUM(deletions) AS total_deletions,
                SUM(additions) - SUM(deletions) AS net_churn,
                COUNT(*) AS commit_count
            FROM {self._table('commits')}
            WHERE repo_id = @repo_id
              AND committed_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
            GROUP BY committed_date
            ORDER BY committed_date
        """
        params = [
            bigquery.ScalarQueryParameter("repo_id", "STRING", repo_id),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
        return await self.query(sql, params)

    async def get_review_cycles(
        self, repo_id: str, days: int = 30
    ) -> list[dict[str, Any]]:
        """Review cycles — rounds per PR, turnaround time."""
        sql = f"""
            SELECT
                pr.created_date,
                pr.number,
                COUNT(r.review_id) AS review_rounds,
                MIN(r.submitted_at) AS first_review_at,
                TIMESTAMP_DIFF(
                    MIN(r.submitted_at), pr.created_at, HOUR
                ) AS hours_to_first_review
            FROM {self._table('pull_requests')} pr
            LEFT JOIN {self._table('reviews')} r
              ON pr.pr_id = r.pr_id AND pr.repo_id = r.repo_id
            WHERE pr.repo_id = @repo_id
              AND pr.created_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
            GROUP BY pr.created_date, pr.number, pr.created_at
            ORDER BY pr.created_date
        """
        params = [
            bigquery.ScalarQueryParameter("repo_id", "STRING", repo_id),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
        return await self.query(sql, params)

    async def get_daily_metrics(
        self, repo_id: str, metric_name: str, days: int = 30
    ) -> list[dict[str, Any]]:
        """Fetch aggregated daily metrics."""
        sql = f"""
            SELECT metric_date, metric_value, developer
            FROM {self._table('daily_metrics')}
            WHERE repo_id = @repo_id
              AND metric_name = @metric_name
              AND metric_date >= DATE_SUB(CURRENT_DATE(), INTERVAL @days DAY)
            ORDER BY metric_date
        """
        params = [
            bigquery.ScalarQueryParameter("repo_id", "STRING", repo_id),
            bigquery.ScalarQueryParameter("metric_name", "STRING", metric_name),
            bigquery.ScalarQueryParameter("days", "INT64", days),
        ]
        return await self.query(sql, params)
