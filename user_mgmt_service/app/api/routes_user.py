"""
API routes for the user management service.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import UserProfileCreate, UserProfileOut, RoleAssignment
from ..models.user_profile import UserProfile
from ..services import user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserProfileOut)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found")
    return profile


@router.post("/profile", response_model=UserProfileOut, status_code=status.HTTP_201_CREATED)
def upsert_profile(profile_in: UserProfileCreate, db: Session = Depends(get_db)):
    profile = user_service.create_or_update_profile(db, profile_in)
    return profile


@router.post("/{user_id}/roles", status_code=status.HTTP_201_CREATED)
def assign_role_endpoint(user_id: int, assignment: RoleAssignment, db: Session = Depends(get_db)):
    # TODO: call auth service to persist role assignment
    record = user_service.assign_role(db, user_id=user_id, role_id=assignment.role_id, assigned_by=assignment.assigned_by)
    return {"message": "Role assigned", "assignment_id": record.id}