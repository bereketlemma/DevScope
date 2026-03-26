"""
Seed BigQuery with 90 days of realistic sample data for development.

Usage:
  python scripts/seed_bigquery.py
"""

from __future__ import annotations

import os
import random
import uuid
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from dotenv import load_dotenv
from google.cloud import bigquery

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "devscope-local")
DATASET = os.getenv("BQ_DATASET", "devscope_dev")
DAYS = 90

# ── Repos to seed ──────────────────────────────────
REPOS = [
    {
        "repo_id": "facebook/react",
        "developers": ["acdlite", "gnoff", "josephsavona", "eps1lon", "rickhanlonii"],
        "daily_prs": (1, 5),
        "daily_commits": (3, 15),
        "pr_latency": (20, 8),
        "churn": (150, 60),
    },
    {
        "repo_id": "microsoft/vscode",
        "developers": ["bpasero", "jrieken", "sandy081", "tyriar", "roblourens", "alexdima"],
        "daily_prs": (3, 10),
        "daily_commits": (10, 30),
        "pr_latency": (16, 6),
        "churn": (300, 120),
    },
]


def _generate_repo_data(repo_cfg: dict, today: date):
    """Generate sample data for a single repository."""
    repo_id = repo_cfg["repo_id"]
    developers = repo_cfg["developers"]
    pr_lo, pr_hi = repo_cfg["daily_prs"]
    commit_lo, commit_hi = repo_cfg["daily_commits"]
    latency_mean, latency_std = repo_cfg["pr_latency"]
    churn_mean, churn_std = repo_cfg["churn"]

    prs = []
    pr_map = {}
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        for _ in range(random.randint(pr_lo, pr_hi)):
            pr_id = str(uuid.uuid4())
            number = random.randint(1, 5000)
            author = random.choice(developers)
            created = datetime.combine(d, datetime.min.time()).replace(
                hour=random.randint(8, 18), tzinfo=timezone.utc
            )
            hours_to_merge = random.gauss(latency_mean, latency_std)
            merged = created + timedelta(hours=max(1, hours_to_merge))

            prs.append({
                "pr_id": pr_id,
                "repo_id": repo_id,
                "number": number,
                "title": f"feat: implement feature #{number}",
                "author": author,
                "state": "merged",
                "created_at": created.isoformat(),
                "first_review_at": (created + timedelta(hours=random.uniform(1, 8))).isoformat(),
                "approved_at": (merged - timedelta(hours=random.uniform(0.5, 2))).isoformat(),
                "merged_at": merged.isoformat(),
                "closed_at": merged.isoformat(),
                "additions": random.randint(10, 500),
                "deletions": random.randint(5, 200),
                "changed_files": random.randint(1, 20),
                "review_rounds": random.randint(1, 4),
                "created_date": d.isoformat(),
            })
            pr_map[number] = pr_id

    commits = []
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        for _ in range(random.randint(commit_lo, commit_hi)):
            committed = datetime.combine(d, datetime.min.time()).replace(
                hour=random.randint(8, 22), tzinfo=timezone.utc
            )
            commits.append({
                "commit_sha": uuid.uuid4().hex[:40],
                "repo_id": repo_id,
                "author": random.choice(developers),
                "message": random.choice([
                    "fix: resolve edge case in parser",
                    "feat: add new API endpoint",
                    "refactor: clean up service layer",
                    "docs: update README",
                    "chore: bump dependencies",
                    "test: add integration tests",
                ]),
                "committed_at": committed.isoformat(),
                "additions": random.randint(5, 300),
                "deletions": random.randint(0, 150),
                "committed_date": d.isoformat(),
            })

    reviews = []
    for number, pr_id in list(pr_map.items())[:200]:
        for _ in range(random.randint(1, 3)):
            reviews.append({
                "review_id": str(uuid.uuid4()),
                "pr_id": pr_id,
                "repo_id": repo_id,
                "reviewer": random.choice(developers),
                "state": random.choice(["APPROVED", "CHANGES_REQUESTED", "COMMENTED"]),
                "submitted_at": datetime.now(timezone.utc).isoformat(),
            })

    daily_metrics = []
    metric_types = [
        ("pr_merge_latency_median", latency_mean, latency_std),
        ("daily_code_churn", churn_mean, churn_std),
        ("review_turnaround_hours", 6, 3),
        ("daily_pr_throughput", (pr_lo + pr_hi) / 2, 2),
    ]
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        for metric_name, mean, std in metric_types:
            value = max(0, random.gauss(mean, std))
            if random.random() < 0.05:
                value *= random.uniform(2.5, 4.0)
            daily_metrics.append({
                "repo_id": repo_id,
                "metric_date": d.isoformat(),
                "metric_name": metric_name,
                "metric_value": round(value, 2),
                "developer": None,
            })

    return prs, commits, reviews, daily_metrics


def seed():
    client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = f"{PROJECT_ID}.{DATASET}"
    today = date.today()

    all_prs, all_commits, all_reviews, all_metrics = [], [], [], []

    for repo_cfg in REPOS:
        prs, commits, reviews, metrics = _generate_repo_data(repo_cfg, today)
        all_prs.extend(prs)
        all_commits.extend(commits)
        all_reviews.extend(reviews)
        all_metrics.extend(metrics)
        print(f"  Generated {repo_cfg['repo_id']}: "
              f"{len(prs)} PRs, {len(commits)} commits, "
              f"{len(reviews)} reviews, {len(metrics)} metrics")

    tables = {
        "pull_requests": all_prs,
        "commits": all_commits,
        "reviews": all_reviews,
        "daily_metrics": all_metrics,
    }

    for table_name, rows in tables.items():
        table_ref = f"{dataset_ref}.{table_name}"
        errors = client.insert_rows_json(table_ref, rows)
        if errors:
            print(f"  ERROR inserting into {table_name}: {errors[:3]}")
        else:
            print(f"  ✓ {table_name}: {len(rows)} rows")

    repo_names = ", ".join(r["repo_id"] for r in REPOS)
    print(f"\nSeed complete — [{repo_names}] with {DAYS} days of data")


if __name__ == "__main__":
    seed()
