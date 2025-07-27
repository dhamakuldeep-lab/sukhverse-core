"""
Auth service API routes.

This router defines endpoints for user registration, login and
retrieving the current user's information.  Role/permission endpoints
are stubbed and can be extended.
"""

from datetime import timedelta
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models.user import User, Role
from ..services import auth as auth_service
from jose import JWTError, jwt

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_service.create_user(db, user_in)
    return schemas.UserOut(id=user.id, email=user.email, status=user.status, roles=[])


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    roles = auth_service.get_user_roles(user)
    token_data = {"sub": str(user.id), "roles": roles}
    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(db, user.id)
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(token_in: schemas.RefreshTokenRequest, db: Session = Depends(get_db)) -> Any:
    """Issue a new access token based on a valid refresh token."""
    user = auth_service.verify_refresh_token(db, token_in.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    roles = auth_service.get_user_roles(user)
    token_data = {"sub": str(user.id), "roles": roles}
    access_token = auth_service.create_access_token(token_data)
    return schemas.Token(access_token=access_token, refresh_token=token_in.refresh_token)


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: User = Depends()) -> Any:  # type: ignore
    """Stub for retrieving the current authenticated user.

    In a real implementation, `current_user` would be provided by
    dependency injection that validates the JWT and fetches the user
    from the database.
    """
    # TODO: implement authentication dependency
    raise HTTPException(status_code=501, detail="Not implemented")