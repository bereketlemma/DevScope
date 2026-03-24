"""Metrics computation service — health scores and aggregations."""

from __future__ import annotations

from typing import Any

from services.bigquery_service import BigQueryService


class MetricsService:
    """Business logic for metric computation and health scoring."""

    def __init__(self, bq: BigQueryService) -> None:
        self._bq = bq

    async def get_health_score(self, repo_id: str, days: int = 30) -> dict[str, Any]:
        """
        Compute a weighted health score (0–100) based on:
          - PR merge latency (30%)
          - Code churn stability (20%)
          - Review coverage (30%)
          - Deployment frequency (20%)
        """
        latency = await self._bq.get_pr_latency(repo_id, days)
        churn = await self._bq.get_code_churn(repo_id, days)
        reviews = await self._bq.get_review_cycles(repo_id, days)

        # Latency score: lower is better (target < 24h median)
        latency_score = 100.0
        if latency:
            avg_median = sum(r.get("median_hours_to_merge", 0) or 0 for r in latency) / len(latency)
            latency_score = max(0, min(100, 100 - (avg_median - 24) * 2))

        # Churn score: stability (low variance is better)
        churn_score = 80.0
        if churn and len(churn) > 1:
            values = [r.get("net_churn", 0) or 0 for r in churn]
            mean_churn = sum(values) / len(values)
            variance = sum((v - mean_churn) ** 2 for v in values) / len(values)
            std_dev = variance ** 0.5
            churn_score = max(0, min(100, 100 - std_dev / 10))

        # Review score: higher review coverage is better
        review_score = 80.0
        if reviews:
            reviewed = sum(1 for r in reviews if (r.get("review_rounds") or 0) > 0)
            review_score = (reviewed / len(reviews)) * 100 if reviews else 0

        # Deployment frequency: more merges is better (target: 1+/day)
        deploy_score = 80.0
        if latency:
            total_prs = sum(r.get("pr_count", 0) or 0 for r in latency)
            daily_avg = total_prs / max(len(latency), 1)
            deploy_score = max(0, min(100, daily_avg * 100))

        # Weighted composite
        health = (
            latency_score * 0.30
            + churn_score * 0.20
            + review_score * 0.30
            + deploy_score * 0.20
        )

        return {
            "health_score": round(health, 1),
            "breakdown": {
                "pr_latency": round(latency_score, 1),
                "code_churn_stability": round(churn_score, 1),
                "review_coverage": round(review_score, 1),
                "deployment_frequency": round(deploy_score, 1),
            },
            "repo_id": repo_id,
            "window_days": days,
        }
