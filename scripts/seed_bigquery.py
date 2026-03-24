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

from google.cloud import bigquery

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "devscope-local")
DATASET = os.getenv("BQ_DATASET", "devscope_dev")
REPO_ID = "bereketlemma/devscope"
DEVELOPERS = ["alice", "bob", "charlie", "diana", "eve"]
DAYS = 90


def seed():
    client = bigquery.Client(project=PROJECT_ID)
    dataset_ref = f"{PROJECT_ID}.{DATASET}"
    today = date.today()

    # ── Pull Requests ──────────────────────────────
    prs = []
    pr_map = {}  # number -> pr_id for reviews
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        num_prs = random.randint(1, 5)
        for _ in range(num_prs):
            pr_id = str(uuid.uuid4())
            number = random.randint(1, 2000)
            author = random.choice(DEVELOPERS)
            created = datetime.combine(d, datetime.min.time()).replace(
                hour=random.randint(8, 18), tzinfo=timezone.utc
            )
            hours_to_merge = random.gauss(24, 12)
            merged = created + timedelta(hours=max(1, hours_to_merge))

            prs.append({
                "pr_id": pr_id,
                "repo_id": REPO_ID,
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

    # ── Commits ────────────────────────────────────
    commits = []
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        num_commits = random.randint(3, 15)
        for _ in range(num_commits):
            committed = datetime.combine(d, datetime.min.time()).replace(
                hour=random.randint(8, 22), tzinfo=timezone.utc
            )
            commits.append({
                "commit_sha": uuid.uuid4().hex[:40],
                "repo_id": REPO_ID,
                "author": random.choice(DEVELOPERS),
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

    # ── Reviews ────────────────────────────────────
    reviews = []
    for number, pr_id in list(pr_map.items())[:200]:
        num_reviews = random.randint(1, 3)
        for _ in range(num_reviews):
            reviews.append({
                "review_id": str(uuid.uuid4()),
                "pr_id": pr_id,
                "repo_id": REPO_ID,
                "reviewer": random.choice(DEVELOPERS),
                "state": random.choice(["APPROVED", "CHANGES_REQUESTED", "COMMENTED"]),
                "submitted_at": datetime.now(timezone.utc).isoformat(),
            })

    # ── Daily Metrics ──────────────────────────────
    daily_metrics = []
    metric_types = [
        ("pr_merge_latency_median", 20, 8),
        ("daily_code_churn", 150, 60),
        ("review_turnaround_hours", 6, 3),
        ("daily_pr_throughput", 4, 2),
    ]
    for day_offset in range(DAYS):
        d = today - timedelta(days=day_offset)
        for metric_name, mean, std in metric_types:
            value = max(0, random.gauss(mean, std))
            # Inject a few anomalies
            if random.random() < 0.05:
                value *= random.uniform(2.5, 4.0)
            daily_metrics.append({
                "repo_id": REPO_ID,
                "metric_date": d.isoformat(),
                "metric_name": metric_name,
                "metric_value": round(value, 2),
                "developer": None,
            })

    # ── Insert into BigQuery ───────────────────────
    tables = {
        "pull_requests": prs,
        "commits": commits,
        "reviews": reviews,
        "daily_metrics": daily_metrics,
    }

    for table_name, rows in tables.items():
        table_ref = f"{dataset_ref}.{table_name}"
        errors = client.insert_rows_json(table_ref, rows)
        if errors:
            print(f"  ERROR inserting into {table_name}: {errors[:3]}")
        else:
            print(f"  ✓ {table_name}: {len(rows)} rows")

    print(f"\nSeed complete — {REPO_ID} with {DAYS} days of data")


if __name__ == "__main__":
    seed()
