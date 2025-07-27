"""
Pydantic models for the user management service.
"""

from typing import Optional, List
from pydantic import BaseModel


class UserProfileBase(BaseModel):
    bio: Optional[str] = None
    contact_number: Optional[str] = None
    department: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileOut(UserProfileBase):
    user_id: int
    created_at: Optional[str]

    class Config:
        orm_mode = True


class RoleAssignment(BaseModel):
    role_id: int
    assigned_by: int