"""Authentication endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.core.security import create_access_token
from app.schemas.user import UserLogin, UserResponse

router = APIRouter()


@router.post("/login")
async def login(user_login: UserLogin, session: AsyncSession = Depends(get_session)) -> dict:
    """GitHub OAuth callback."""
    # TODO: Exchange authorization code for GitHub access token
    # TODO: Fetch user data from GitHub
    # TODO: Create or update user in database
    # TODO: Return JWT token
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/me", response_model=UserResponse)
async def get_current_user(session: AsyncSession = Depends(get_session)) -> dict:
    """Get current authenticated user."""
    # TODO: Verify JWT token
    # TODO: Fetch user from database
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/logout")
async def logout() -> dict:
    """Logout endpoint."""
    return {"message": "Logged out successfully"}
