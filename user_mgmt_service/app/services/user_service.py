"""
Business logic for the user management service.
"""

from sqlalchemy.orm import Session
from ..models.user_profile import UserProfile, BulkUploadLog, UserRoleAssignment
from ..schemas.user import UserProfileCreate
from ..events.producer import publish_event


def create_or_update_profile(db: Session, profile_in: UserProfileCreate) -> UserProfile:
    profile = db.query(UserProfile).filter(UserProfile.user_id == profile_in.user_id).first()
    if profile:
        # Update existing profile
        profile.bio = profile_in.bio
        profile.contact_number = profile_in.contact_number
        profile.department = profile_in.department
    else:
        profile = UserProfile(
            user_id=profile_in.user_id,
            bio=profile_in.bio,
            contact_number=profile_in.contact_number,
            department=profile_in.department,
        )
        db.add(profile)
    db.commit()
    db.refresh(profile)
    publish_event("user_profile_updated", {"user_id": profile.user_id})
    return profile


def assign_role(db: Session, user_id: int, role_id: int, assigned_by: int) -> UserRoleAssignment:
    assignment = UserRoleAssignment(user_id=user_id, role_id=role_id, assigned_by=assigned_by)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    publish_event("role_assigned", {"user_id": user_id, "role_id": role_id, "assigned_by": assigned_by})
    return assignment