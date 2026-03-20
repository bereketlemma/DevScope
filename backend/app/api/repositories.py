"""Repository endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.schemas.repository import RepositoryResponse

router = APIRouter()


@router.get("/", response_model=list[RepositoryResponse])
async def list_repositories(
    skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_session)
) -> list:
    """List repositories."""
    # TODO: Fetch repositories from database
    # TODO: Apply pagination
    return []


@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(repo_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    """Get repository by ID."""
    # TODO: Fetch repository from database
    raise HTTPException(status_code=404, detail="Repository not found")


@router.post("/sync/{repo_id}")
async def sync_repository(repo_id: int, session: AsyncSession = Depends(get_session)) -> dict:
    """Trigger repository sync."""
    # TODO: Create sync job
    # TODO: Enqueue Celery task
    return {"status": "sync started", "repo_id": repo_id}
