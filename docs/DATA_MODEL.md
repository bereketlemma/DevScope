# Data Model

## PostgreSQL Schema

### users

Stores authenticated users from GitHub.

| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY |
| github_id | INTEGER | UNIQUE, NOT NULL |
| username | VARCHAR(255) | UNIQUE, NOT NULL |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| avatar_url | VARCHAR(2048) | NOT NULL |
| access_token | VARCHAR(1024) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### repositories

Stores user's repositories synced from GitHub.

| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY |
| github_id | INTEGER | UNIQUE, NOT NULL |
| owner | VARCHAR(255) | NOT NULL |
| name | VARCHAR(255) | NOT NULL |
| full_name | VARCHAR(511) | UNIQUE, NOT NULL |
| url | VARCHAR(2048) | NOT NULL |
| description | TEXT | NULLABLE |
| stars | INTEGER | DEFAULT 0 |
| watchers | INTEGER | DEFAULT 0 |
| forks | INTEGER | DEFAULT 0 |
| language | VARCHAR(255) | NULLABLE |
| is_fork | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |
| last_synced_at | TIMESTAMP | NULLABLE |

### sync_jobs

Tracks background sync task status.

| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY |
| repository_id | INTEGER | NOT NULL, FK(repositories) |
| status | ENUM | DEFAULT 'pending' |
| error_message | VARCHAR(1024) | NULLABLE |
| started_at | TIMESTAMP | NULLABLE |
| completed_at | TIMESTAMP | NULLABLE |
| created_at | TIMESTAMP | DEFAULT NOW() |

**Enum values:** pending, running, success, failed

### anomalies

Stores detected anomalies for metrics.

| Column | Type | Constraint |
|--------|------|-----------|
| id | INTEGER | PRIMARY KEY |
| repository_id | INTEGER | NOT NULL, FK(repositories) |
| metric_name | VARCHAR(255) | NOT NULL |
| detected_value | FLOAT | NOT NULL |
| z_score | FLOAT | NOT NULL |
| threshold | FLOAT | NOT NULL |
| description | TEXT | NULLABLE |
| created_at | TIMESTAMP | DEFAULT NOW() |

## BigQuery Schema

### pull_requests

Raw pull request events.

| Column | Type | Description |
|--------|------|-----------|
| event_id | STRING | Unique event ID |
| repository_id | INTEGER | Reference to repo |
| pr_number | INTEGER | PR number |
| author | STRING | PR author |
| title | STRING | PR title |
| state | STRING | open, closed, merged |
| created_at | TIMESTAMP | Creation time |
| closed_at | TIMESTAMP | Closure/merge time |
| review_comments | INTEGER | Number of reviews |
| additions | INTEGER | Lines added |
| deletions | INTEGER | Lines deleted |

**Partitioning:** created_at (daily)

**Clustering:** repository_id, state

### commits

Raw commit events.

| Column | Type | Description |
|--------|------|-----------|
| event_id | STRING | Unique event ID |
| repository_id | INTEGER | Reference to repo |
| sha | STRING | Commit SHA |
| author | STRING | Commit author |
| message | STRING | Commit message |
| created_at | TIMESTAMP | Commit time |
| files_changed | INTEGER | Changed files |
| insertions | INTEGER | Lines added |
| deletions | INTEGER | Lines deleted |

**Partitioning:** created_at (daily)

**Clustering:** repository_id, author

### reviews

Pull request review events.

| Column | Type | Description |
|--------|------|-----------|
| event_id | STRING | Unique event ID |
| pr_number | INTEGER | PR number |
| reviewer | STRING | Reviewer name |
| state | STRING | approved, changes_requested, commented |
| submitted_at | TIMESTAMP | Review time |
| repository_id | INTEGER | Reference to repo |

**Partitioning:** submitted_at (daily)

**Clustering:** repository_id, pr_number

## Relationships

```
users
  ├── 1:N repositories
  │   ├── 1:N sync_jobs
  │   └── 1:N anomalies

BigQuery (repositories)
  ├── 1:N pull_requests
  ├── 1:N commits
  └── 1:N reviews
```

## Metrics Calculated from BigQuery

### PR Latency
Time from PR creation to merge/close.

```sql
AVG(TIMESTAMP_DIFF(closed_at, created_at, DAY)) as pr_latency_days
```

### Review Cycle Time
Time from PR creation to first review.

```sql
AVG(TIMESTAMP_DIFF(first_review_at, created_at, HOUR)) as review_cycle_hours
```

### Commit Frequency
Commits per day over past 30 days.

```sql
COUNT(*) / 30 as commits_per_day
```

### PR Acceptance Rate
Merged PRs / Total PRs.

```sql
COUNT(CASE WHEN state = 'merged' THEN 1 END) / COUNT(*) as acceptance_rate
```

## Anomaly Detection

Using **Z-score method**:

For each metric over 30 days:

$$\text{z} = \frac{x - \mu}{\sigma}$$

Where:
- $ x $ = detected value
- $ \mu $ = mean
- $ \sigma $ = standard deviation

**Threshold:** $ |z| > 3 $ (99.7% confidence)

Example: If PR latency averages 2 days with 0.5 std dev, a 3.5-day PR would be flagged:

$$z = \frac{3.5 - 2}{0.5} = 3.0 \text{ (anomaly)}$$
