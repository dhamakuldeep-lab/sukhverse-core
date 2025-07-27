"""
Pydantic models for requests and responses in the auth service.
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, constr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str]


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    user_id: int
    roles: List[str]


class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    """Payload for changing a user's password."""

    old_password: str
    new_password: constr(min_length=8)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    status: str
    roles: List[str]

    class Config:
        orm_mode = True