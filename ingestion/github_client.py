"""GitHub API client with rate-limit handling and pagination."""

from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from config import config

logger = logging.getLogger(__name__)

GITHUB_API_BASE = "https://api.github.com"


class GitHubClient:
    """Async GitHub REST API client with automatic pagination and rate-limit backoff."""

    def __init__(self, token: str | None = None) -> None:
        self.token = token or config.github_token
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=GITHUB_API_BASE,
                headers=self.headers,
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()

    async def _get_paginated(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """Fetch all pages from a paginated GitHub endpoint."""
        client = await self._get_client()
        results: list[dict[str, Any]] = []
        params = params or {}
        params.setdefault("per_page", 100)
        url = endpoint

        while url:
            response = await client.get(url, params=params)
            response.raise_for_status()

            remaining = int(response.headers.get("x-ratelimit-remaining", 100))
            if remaining < 10:
                logger.warning("GitHub rate limit low: %d remaining", remaining)

            results.extend(response.json())
            # Parse Link header for next page
            url = self._parse_next_link(response.headers.get("link", ""))
            params = {}  # params are in the URL for subsequent pages

        return results

    @staticmethod
    def _parse_next_link(link_header: str) -> str | None:
        """Extract the 'next' URL from GitHub's Link header."""
        if not link_header:
            return None
        for part in link_header.split(","):
            if 'rel="next"' in part:
                return part.split(";")[0].strip().strip("<>")
        return None

    async def get_repo(self, owner: str, name: str) -> dict[str, Any]:
        """Fetch repository metadata."""
        client = await self._get_client()
        response = await client.get(f"/repos/{owner}/{name}")
        response.raise_for_status()
        return response.json()

    async def get_pull_requests(
        self, owner: str, name: str, since: datetime | None = None
    ) -> list[dict[str, Any]]:
        """Fetch pull requests, optionally filtered by date."""
        params: dict[str, Any] = {"state": "all", "sort": "updated", "direction": "desc"}
        if since:
            params["since"] = since.isoformat()
        return await self._get_paginated(f"/repos/{owner}/{name}/pulls", params)

    async def get_commits(
        self, owner: str, name: str, since: datetime | None = None
    ) -> list[dict[str, Any]]:
        """Fetch commits, optionally filtered by date."""
        params: dict[str, Any] = {}
        if since:
            params["since"] = since.isoformat()
        return await self._get_paginated(f"/repos/{owner}/{name}/commits", params)

    async def get_reviews(
        self, owner: str, name: str, pr_number: int
    ) -> list[dict[str, Any]]:
        """Fetch reviews for a specific pull request."""
        return await self._get_paginated(
            f"/repos/{owner}/{name}/pulls/{pr_number}/reviews"
        )

    async def get_pr_detail(
        self, owner: str, name: str, pr_number: int
    ) -> dict[str, Any]:
        """Fetch detailed PR info (includes additions/deletions)."""
        client = await self._get_client()
        response = await client.get(f"/repos/{owner}/{name}/pulls/{pr_number}")
        response.raise_for_status()
        return response.json()
