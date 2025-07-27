"""
📄 File: auth_service/app/api/routes_auth.py

Auth service API routes.

This router defines endpoints for user registration, login, refreshing tokens,
changing passwords, and password reset. Role/permission endpoints are stubbed and can be extended.
"""

from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..models.user import User
from ..services import auth as auth_service
from ..security.jwt import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ✅ Define the router
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)) -> Any:
    """Register a new user."""
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = auth_service.create_user(db, user_in)
    return schemas.UserOut(id=user.id, email=user.email, status=user.status, roles=[])


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    """Login and get access/refresh tokens."""
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    roles = auth_service.get_user_roles(user)
    access_token = auth_service.create_access_token(user.id, roles)
    refresh_token = auth_service.create_refresh_token(db, user.id)
    return schemas.Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=schemas.Token)
def refresh_token(token_in: schemas.RefreshTokenRequest, db: Session = Depends(get_db)) -> Any:
    """🔁 Legacy alias for `/refresh-token`."""
    user = auth_service.verify_refresh_token(db, token_in.refresh_token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    roles = auth_service.get_user_roles(user)
    access_token = auth_service.create_access_token(user.id, roles)
    return schemas.Token(access_token=access_token, refresh_token=token_in.refresh_token)


# ✅ Merged block: Added by Codex — Change Password, Forgot/Reset Password, Refresh-Token
@router.post("/change-password")
def change_password(
    passwords: schemas.ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Any:
    """Allow an authenticated user to change their password."""
    success = auth_service.change_password(
        db,
        user_id=current_user.id,
        old_password=passwords.old_password,
        new_password=passwords.new_password,
    )
    if not success:
        raise HTTPException(status_code=400, detail="Incorrect password")
    return {"message": "Password updated"}


@router.post("/forgot-password")
def forgot_password(payload: schemas.PasswordResetRequest, db: Session = Depends(get_db)) -> Any:
    """Generate a password reset token for the given email."""
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = auth_service.create_password_reset(db, user.id)
    return {"reset_token": token}


@router.post("/reset-password")
def reset_password(payload: schemas.ResetPasswordRequest, db: Session = Depends(get_db)) -> Any:
    """Reset a user's password using a valid token."""
    success = auth_service.reset_user_password(db, payload.token, payload.new_password)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    return {"message": "Password updated"}


@router.post("/refresh-token", response_model=schemas.Token)
def refresh_token_new(token_in: schemas.RefreshTokenRequest, db: Session = Depends(get_db)) -> Any:
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
