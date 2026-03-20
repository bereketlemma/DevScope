"""Repository Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RepositoryBase(BaseModel):
    """Base repository schema."""

    github_id: int
    owner: str
    name: str
    full_name: str
    url: str


class RepositoryCreate(RepositoryBase):
    """Repository creation schema."""

    description: str | None = None
    stars: int = 0
    watchers: int = 0
    forks: int = 0
    language: str | None = None
    is_fork: bool = False


class RepositoryResponse(RepositoryCreate):
    """Repository response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    last_synced_at: datetime | None = None
