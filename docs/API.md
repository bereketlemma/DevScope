# API Reference

## Base URL

`/api/v1`

## Authentication

All endpoints (except `/auth/login`) require a JWT token in the `Authorization` header:

```bash
Authorization: Bearer <token>
```

## Authentication Endpoints

### POST /auth/login

GitHub OAuth login. Exchanges authorization code for JWT token.

**Request:**
```json
{
  "code": "github_code",
  "state": "state_value"
}
```

**Response:**
```json
{
  "access_token": "jwt_token",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "github_id": 12345,
    "username": "octocat",
    "email": "octocat@github.com",
    "avatar_url": "https://...",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

### GET /auth/me

Get current authenticated user.

**Response:**
```json
{
  "id": 1,
  "github_id": 12345,
  "username": "octocat",
  "email": "octocat@github.com",
  "avatar_url": "https://...",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### POST /auth/logout

Logout (client-side token removal).

## Repository Endpoints

### GET /repositories

List user's repositories.

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Number of records to return (default: 10)

**Response:**
```json
[
  {
    "id": 1,
    "github_id": 12345,
    "owner": "octocat",
    "name": "Hello-World",
    "full_name": "octocat/Hello-World",
    "url": "https://github.com/octocat/Hello-World",
    "description": "Repository description",
    "stars": 80,
    "watchers": 80,
    "forks": 9,
    "language": "Python",
    "is_fork": false,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "last_synced_at": "2024-01-05T12:00:00Z"
  }
]
```

### GET /repositories/{repo_id}

Get repository details.

**Response:** Repository object (see above)

### POST /repositories/{repo_id}/sync

Trigger repository data sync.

**Response:**
```json
{
  "status": "sync started",
  "repo_id": 1,
  "sync_job_id": 42
}
```

## Metrics Endpoints

### GET /metrics/{repo_id}

Get repository metrics snapshot.

**Response:**
```json
{
  "repository_id": 1,
  "pr_latency_days": 2.5,
  "pr_review_time_hours": 4.2,
  "commit_frequency_daily": 1.3,
  "pr_acceptance_rate": 0.92
}
```

### GET /metrics/{repo_id}/daily

Get daily metric history.

**Query Parameters:**
- `days`: Number of days to retrieve (default: 30)

**Response:**
```json
[
  {
    "date": "2024-01-05",
    "metric_name": "pr_count",
    "value": 5,
    "avg_value": 3.2,
    "median_value": 3,
    "p95_value": 8
  }
]
```

### GET /metrics/{repo_id}/anomalies

Get detected anomalies for repository.

**Response:**
```json
{
  "anomalies": [
    {
      "id": 1,
      "repository_id": 1,
      "metric_name": "pr_latency_days",
      "detected_value": 15.2,
      "z_score": 3.5,
      "threshold": 3.0,
      "description": "Unusually high PR latency",
      "created_at": "2024-01-05T10:30:00Z"
    }
  ]
}
```

## Error Responses

All endpoints return error responses in this format:

```json
{
  "detail": "Error message"
}
```

### Status Codes

- `200`: Success
- `201`: Created
- `400`: Bad request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not found
- `500`: Server error

## Rate Limiting

No built-in rate limiting in Milestone 1. GitHub API has standard rate limits (60 requests/hour unauthenticated, 5000/hour authenticated).

## Pagination

Use `skip` and `limit` parameters for pagination. Example:

```bash
GET /api/v1/repositories?skip=0&limit=10
```
