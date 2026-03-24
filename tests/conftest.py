"""Shared test fixtures."""

import pytest


@pytest.fixture
def sample_pr_payload():
    """Sample GitHub PR payload for testing."""
    return {
        "id": 123456,
        "number": 42,
        "title": "feat: add user auth",
        "user": {"login": "bereketlemma"},
        "state": "closed",
        "created_at": "2026-03-01T10:00:00Z",
        "merged_at": "2026-03-02T14:30:00Z",
        "closed_at": "2026-03-02T14:30:00Z",
        "additions": 250,
        "deletions": 80,
        "changed_files": 12,
    }


@pytest.fixture
def sample_commit_payload():
    """Sample GitHub commit payload."""
    return {
        "sha": "abc123def456",
        "author": {"login": "bereketlemma"},
        "commit": {
            "message": "feat: add login endpoint",
            "committer": {"date": "2026-03-01T12:00:00Z"},
        },
        "stats": {"additions": 100, "deletions": 20},
    }


@pytest.fixture
def sample_review_payload():
    """Sample GitHub review payload."""
    return {
        "id": 789,
        "pull_request_url": "https://api.github.com/repos/owner/repo/pulls/42",
        "user": {"login": "alice"},
        "state": "APPROVED",
        "submitted_at": "2026-03-01T16:00:00Z",
    }
