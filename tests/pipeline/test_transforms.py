"""Tests for Apache Beam transforms."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "pipeline"))

from transforms import TransformPullRequest, TransformCommit, TransformReview


class TestTransformPullRequest:
    def test_transforms_pr_payload(self, sample_pr_payload):
        transform = TransformPullRequest()
        element = {"raw": sample_pr_payload, "repo_id": "owner/repo"}
        results = list(transform.process(element))

        assert len(results) == 1
        row = results[0]
        assert row["pr_id"] == "123456"
        assert row["repo_id"] == "owner/repo"
        assert row["author"] == "bereketlemma"
        assert row["additions"] == 250
        assert row["deletions"] == 80
        assert row["created_date"] == "2026-03-01"

    def test_handles_missing_dates(self):
        transform = TransformPullRequest()
        element = {
            "raw": {"id": 1, "number": 1, "user": {"login": "test"}, "state": "open"},
            "repo_id": "owner/repo",
        }
        results = list(transform.process(element))
        assert len(results) == 1
        assert results[0]["created_date"] is None


class TestTransformCommit:
    def test_transforms_commit_payload(self, sample_commit_payload):
        transform = TransformCommit()
        element = {"raw": sample_commit_payload, "repo_id": "owner/repo"}
        results = list(transform.process(element))

        assert len(results) == 1
        row = results[0]
        assert row["commit_sha"] == "abc123def456"
        assert row["author"] == "bereketlemma"
        assert row["additions"] == 100
        assert row["committed_date"] == "2026-03-01"


class TestTransformReview:
    def test_transforms_review_payload(self, sample_review_payload):
        transform = TransformReview()
        element = {"raw": sample_review_payload, "repo_id": "owner/repo"}
        results = list(transform.process(element))

        assert len(results) == 1
        row = results[0]
        assert row["review_id"] == "789"
        assert row["reviewer"] == "alice"
        assert row["state"] == "APPROVED"
        assert row["pr_id"] == "42"
