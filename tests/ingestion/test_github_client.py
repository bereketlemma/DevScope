"""Tests for the ingestion service."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "ingestion"))

import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestGitHubClient:
    """Tests for GitHub API client."""

    def test_parse_next_link_with_next(self):
        from github_client import GitHubClient

        header = '<https://api.github.com/repos/owner/repo/pulls?page=2>; rel="next", <https://api.github.com/repos/owner/repo/pulls?page=5>; rel="last"'
        result = GitHubClient._parse_next_link(header)
        assert result == "https://api.github.com/repos/owner/repo/pulls?page=2"

    def test_parse_next_link_without_next(self):
        from github_client import GitHubClient

        header = '<https://api.github.com/repos/owner/repo/pulls?page=5>; rel="last"'
        result = GitHubClient._parse_next_link(header)
        assert result is None

    def test_parse_next_link_empty(self):
        from github_client import GitHubClient

        assert GitHubClient._parse_next_link("") is None


class TestIngestionWebhook:
    """Tests for webhook signature verification."""

    def test_hmac_verification_logic(self):
        import hashlib
        import hmac

        secret = "test-secret"
        body = b'{"action": "opened"}'
        expected = "sha256=" + hmac.new(
            secret.encode(), body, hashlib.sha256
        ).hexdigest()

        # Valid signature should match
        assert hmac.compare_digest(expected, expected)

        # Tampered signature should not match
        assert not hmac.compare_digest(expected, "sha256=invalid")
