"""User Pydantic schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    """Base user schema."""

    github_id: int
    username: str
    email: str
    avatar_url: str


class UserCreate(UserBase):
    """User creation schema."""

    access_token: str


class UserResponse(UserBase):
    """User response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserLogin(BaseModel):
    """User login schema."""

    code: str
    state: str
