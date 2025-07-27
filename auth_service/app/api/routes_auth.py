"""
Auth service API routes.

This router defines endpoints for user registration, login and
retrieving the current user's information.  Role/permission endpoints
are stubbed and can be extended.
"""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models.user import User
from ..services import auth as auth_service
from ..security.jwt import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

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
    access_token = auth_service.create_access_token(user.id, roles)
    refresh_token = auth_service.create_refresh_token(db, user.id)
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(token_in: schemas.RefreshTokenRequest, db: Session = Depends(get_db)) -> Any:
    """Issue a new access token based on a valid refresh token."""
    user = auth_service.verify_refresh_token(db, token_in.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    roles = auth_service.get_user_roles(user)
    access_token = auth_service.create_access_token(user.id, roles)
    return schemas.Token(access_token=access_token, refresh_token=token_in.refresh_token)


@router.get("/me", response_model=schemas.UserOut)
def read_users_me(current_user: User = Depends(get_current_user)) -> Any:
    """Return the currently authenticated user's information."""
    roles = auth_service.get_user_roles(current_user)
    return schemas.UserOut(
        id=current_user.id,
        email=current_user.email,
        status=current_user.status,
        roles=roles,
    )

