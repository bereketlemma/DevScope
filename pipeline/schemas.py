"""BigQuery table schemas for DevScope analytics data."""

# Schema for pull_requests table (partitioned by created_date, clustered by repo_id)
PULL_REQUESTS_SCHEMA = [
    {"name": "pr_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "repo_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "number", "type": "INT64", "mode": "NULLABLE"},
    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
    {"name": "author", "type": "STRING", "mode": "NULLABLE"},
    {"name": "state", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "first_review_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "approved_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "merged_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "closed_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "additions", "type": "INT64", "mode": "NULLABLE"},
    {"name": "deletions", "type": "INT64", "mode": "NULLABLE"},
    {"name": "changed_files", "type": "INT64", "mode": "NULLABLE"},
    {"name": "review_rounds", "type": "INT64", "mode": "NULLABLE"},
    {"name": "created_date", "type": "DATE", "mode": "NULLABLE"},
]

# Schema for commits table (partitioned by committed_date, clustered by repo_id)
COMMITS_SCHEMA = [
    {"name": "commit_sha", "type": "STRING", "mode": "REQUIRED"},
    {"name": "repo_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "author", "type": "STRING", "mode": "NULLABLE"},
    {"name": "message", "type": "STRING", "mode": "NULLABLE"},
    {"name": "committed_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "additions", "type": "INT64", "mode": "NULLABLE"},
    {"name": "deletions", "type": "INT64", "mode": "NULLABLE"},
    {"name": "committed_date", "type": "DATE", "mode": "NULLABLE"},
]

# Schema for reviews table (clustered by repo_id)
REVIEWS_SCHEMA = [
    {"name": "review_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "pr_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "repo_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "reviewer", "type": "STRING", "mode": "NULLABLE"},
    {"name": "state", "type": "STRING", "mode": "NULLABLE"},
    {"name": "submitted_at", "type": "TIMESTAMP", "mode": "NULLABLE"},
]

# Schema for daily_metrics table (partitioned by metric_date, clustered by repo_id)
DAILY_METRICS_SCHEMA = [
    {"name": "repo_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "metric_date", "type": "DATE", "mode": "REQUIRED"},
    {"name": "metric_name", "type": "STRING", "mode": "REQUIRED"},
    {"name": "metric_value", "type": "FLOAT64", "mode": "NULLABLE"},
    {"name": "developer", "type": "STRING", "mode": "NULLABLE"},
]
