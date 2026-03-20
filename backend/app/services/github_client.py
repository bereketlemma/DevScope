"""GitHub API client."""
import logging
from typing import Any

import httpx

from app.core.config import settings

logger = logging.getLogger(__name__)


class GitHubClient:
    """GitHub API client."""

    BASE_URL = "https://api.github.com"

    def __init__(self, access_token: str) -> None:
        """Initialize GitHub client."""
        self.access_token = access_token
        self.headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def get_user(self) -> dict[str, Any]:
        """Get authenticated user data."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/user",
                headers=self.headers,
            )
            response.raise_for_status()
            return response.json()

    async def get_repositories(self) -> list[dict[str, Any]]:
        """Get user repositories."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/user/repos",
                headers=self.headers,
                params={"per_page": 100},
            )
            response.raise_for_status()
            return response.json()

    async def get_pulls(self, owner: str, repo: str) -> list[dict[str, Any]]:
        """Get pull requests."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/pulls",
                headers=self.headers,
                params={"state": "all", "per_page": 100},
            )
            response.raise_for_status()
            return response.json()

    async def get_commits(self, owner: str, repo: str) -> list[dict[str, Any]]:
        """Get commits."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/repos/{owner}/{repo}/commits",
                headers=self.headers,
                params={"per_page": 100},
            )
            response.raise_for_status()
            return response.json()
