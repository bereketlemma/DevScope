"""
Ingestion Service — Cloud Run

Fetches GitHub repository data (PRs, commits, reviews) and publishes
structured events to Cloud Pub/Sub for downstream processing via Dataflow.

Endpoints:
  POST /ingest/{owner}/{repo}   — trigger full backfill for a repo
  POST /sync/{owner}/{repo}     — incremental sync since last run
  POST /webhooks/github         — real-time webhook receiver
  GET  /health                  — liveness check
"""

from __future__ import annotations

import hashlib
import hmac
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from pydantic import BaseModel

from config import config
from github_client import GitHubClient
from publisher import EventPublisher

logging.basicConfig(level=config.log_level)
logger = logging.getLogger(__name__)

# ─── Lifespan ──────────────────────────────────────
github = GitHubClient()
publisher = EventPublisher()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Ingestion service starting (env=%s)", config.environment)
    yield
    await github.close()
    logger.info("Ingestion service stopped")


app = FastAPI(
    title="DevScope Ingestion Service",
    version="0.1.0",
    lifespan=lifespan,
)


# ─── Schemas ───────────────────────────────────────
class IngestResponse(BaseModel):
    status: str
    repo: str
    message: str


class HealthResponse(BaseModel):
    status: str
    service: str


# ─── Ingestion Logic ──────────────────────────────
async def _ingest_repo(
    owner: str, repo: str, since: datetime | None = None
) -> dict[str, int]:
    """Fetch GitHub data and publish events to Pub/Sub."""
    repo_id = f"{owner}/{repo}"
    counts = {"pull_requests": 0, "commits": 0, "reviews": 0}

    # 1. Fetch and publish pull requests
    prs = await github.get_pull_requests(owner, repo, since=since)
    for pr in prs:
        detail = await github.get_pr_detail(owner, repo, pr["number"])
        await publisher.publish_event("pull_request", repo_id, detail)
        counts["pull_requests"] += 1

        # 2. Fetch and publish reviews for each PR
        reviews = await github.get_reviews(owner, repo, pr["number"])
        for review in reviews:
            await publisher.publish_event("review", repo_id, review)
            counts["reviews"] += 1

    # 3. Fetch and publish commits
    commits = await github.get_commits(owner, repo, since=since)
    for commit in commits:
        await publisher.publish_event("commit", repo_id, commit)
        counts["commits"] += 1

    logger.info("Ingested %s: %s", repo_id, counts)
    return counts


# ─── Routes ────────────────────────────────────────
@app.post("/ingest/{owner}/{repo}", response_model=IngestResponse)
async def ingest_repo(owner: str, repo: str, background_tasks: BackgroundTasks):
    """Trigger a full historical backfill (last N days)."""
    since = datetime.now(timezone.utc) - timedelta(days=config.default_lookback_days)
    background_tasks.add_task(_ingest_repo, owner, repo, since)
    return IngestResponse(
        status="accepted",
        repo=f"{owner}/{repo}",
        message=f"Backfill started for last {config.default_lookback_days} days",
    )


@app.post("/sync/{owner}/{repo}", response_model=IngestResponse)
async def sync_repo(owner: str, repo: str, background_tasks: BackgroundTasks):
    """Incremental sync — fetches events from last 24 hours."""
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    background_tasks.add_task(_ingest_repo, owner, repo, since)
    return IngestResponse(
        status="accepted",
        repo=f"{owner}/{repo}",
        message="Incremental sync started (last 24h)",
    )


@app.post("/webhooks/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    """Receive real-time GitHub webhook events and publish to Pub/Sub."""
    # Verify HMAC signature
    signature = request.headers.get("x-hub-signature-256", "")
    body = await request.body()

    if config.github_webhook_secret:
        expected = (
            "sha256="
            + hmac.new(
                config.github_webhook_secret.encode(),
                body,
                hashlib.sha256,
            ).hexdigest()
        )
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=401, detail="Invalid signature")

    event_type = request.headers.get("x-github-event", "unknown")
    payload = json.loads(body)
    repo_id = payload.get("repository", {}).get("full_name", "unknown")

    # Map GitHub webhook events to our event types
    event_map = {
        "pull_request": "pull_request",
        "push": "commit",
        "pull_request_review": "review",
    }
    mapped_type = event_map.get(event_type)

    if mapped_type:
        background_tasks.add_task(
            publisher.publish_event, mapped_type, repo_id, payload
        )

    return {"status": "received", "event_type": event_type}


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="healthy", service="ingestion")
