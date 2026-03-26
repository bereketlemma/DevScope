"""Custom Apache Beam PTransforms for GitHub event processing."""

from __future__ import annotations

import json
import logging
from datetime import datetime
from typing import Any

import apache_beam as beam

logger = logging.getLogger(__name__)


class ParsePubSubMessage(beam.DoFn):
    """Parse raw Pub/Sub message bytes into a structured dict."""

    def process(self, element: bytes) -> list[dict[str, Any]]:
        try:
            message = json.loads(element.decode("utf-8"))
            yield message
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error("Failed to parse message: %s", e)


class RoutByEventType(beam.DoFn):
    """Tag events by type for routing to different BigQuery tables."""

    def process(self, element: dict[str, Any]):
        event_type = element.get("event_type", "unknown")
        payload = element.get("payload", {})
        repo_id = element.get("repo_id", "")

        if event_type == "pull_request":
            yield beam.pvalue.TaggedOutput(
                "pull_requests",
                {
                    "raw": payload,
                    "repo_id": repo_id,
                },
            )
        elif event_type == "commit":
            yield beam.pvalue.TaggedOutput(
                "commits",
                {
                    "raw": payload,
                    "repo_id": repo_id,
                },
            )
        elif event_type == "review":
            yield beam.pvalue.TaggedOutput(
                "reviews",
                {
                    "raw": payload,
                    "repo_id": repo_id,
                },
            )
        else:
            logger.warning("Unknown event type: %s", event_type)


class TransformPullRequest(beam.DoFn):
    """Transform raw GitHub PR payload into BigQuery row."""

    def process(self, element: dict[str, Any]) -> list[dict[str, Any]]:
        raw = element["raw"]
        repo_id = element["repo_id"]

        created_at = raw.get("created_at")
        created_date = None
        if created_at:
            try:
                created_date = datetime.fromisoformat(
                    created_at.replace("Z", "+00:00")
                ).strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                pass

        yield {
            "pr_id": str(raw.get("id", "")),
            "repo_id": repo_id,
            "number": raw.get("number"),
            "title": raw.get("title", ""),
            "author": raw.get("user", {}).get("login", ""),
            "state": raw.get("state", ""),
            "created_at": created_at,
            "first_review_at": None,  # Enriched later or via review events
            "approved_at": None,
            "merged_at": raw.get("merged_at"),
            "closed_at": raw.get("closed_at"),
            "additions": raw.get("additions", 0),
            "deletions": raw.get("deletions", 0),
            "changed_files": raw.get("changed_files", 0),
            "review_rounds": 0,
            "created_date": created_date,
        }


class TransformCommit(beam.DoFn):
    """Transform raw GitHub commit payload into BigQuery row."""

    def process(self, element: dict[str, Any]) -> list[dict[str, Any]]:
        raw = element["raw"]
        repo_id = element["repo_id"]

        commit_data = raw.get("commit", {})
        committed_at = commit_data.get("committer", {}).get("date")
        committed_date = None
        if committed_at:
            try:
                committed_date = datetime.fromisoformat(
                    committed_at.replace("Z", "+00:00")
                ).strftime("%Y-%m-%d")
            except (ValueError, AttributeError):
                pass

        yield {
            "commit_sha": raw.get("sha", ""),
            "repo_id": repo_id,
            "author": raw.get("author", {}).get("login", "")
            if raw.get("author")
            else "",
            "message": commit_data.get("message", ""),
            "committed_at": committed_at,
            "additions": raw.get("stats", {}).get("additions", 0),
            "deletions": raw.get("stats", {}).get("deletions", 0),
            "committed_date": committed_date,
        }


class TransformReview(beam.DoFn):
    """Transform raw GitHub review payload into BigQuery row."""

    def process(self, element: dict[str, Any]) -> list[dict[str, Any]]:
        raw = element["raw"]
        repo_id = element["repo_id"]

        yield {
            "review_id": str(raw.get("id", "")),
            "pr_id": str(raw.get("pull_request_url", "").split("/")[-1]),
            "repo_id": repo_id,
            "reviewer": raw.get("user", {}).get("login", ""),
            "state": raw.get("state", ""),
            "submitted_at": raw.get("submitted_at"),
        }
