"""
📄 File: auth_service/app/services/auth.py

Business logic for authentication and user management in the auth service.
"""

from datetime import datetime, timedelta
from typing import List, Optional

import os
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import schemas
from ..models.user import User, RefreshToken, PasswordReset, Role
from ..utils.security import hash_password, verify_password
from ..events.producer import publish_event

# ✅ Secure loading of JWT-related environment variables
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise EnvironmentError("JWT_SECRET_KEY environment variable is required")

JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"])
    if ACCESS_TOKEN_EXPIRE_MINUTES <= 0:
        raise ValueError
except KeyError as exc:
    raise EnvironmentError(
        "ACCESS_TOKEN_EXPIRE_MINUTES environment variable is required"
    ) from exc
except ValueError as exc:
    raise ValueError(
        "ACCESS_TOKEN_EXPIRE_MINUTES must be a positive integer"
    ) from exc

REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))


def create_user(db: Session, user_in: schemas.UserCreate) -> User:
    """Create a new user account and emit a UserRegistered event."""
    user = User(email=user_in.email, password_hash=hash_password(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    # Publish event to Kafka
    publish_event("user_registered", {"user_id": user.id, "email": user.email})
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Verify user credentials and return the user if valid."""
    user: User | None = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def create_access_token(user_id: int, roles: List[str], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token embedding the user's roles."""
    to_encode = {"sub": str(user_id), "roles": roles}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(db: Session, user_id: int, device_info: str | None = None) -> str:
    """Generate and persist a refresh token for a user."""
    import uuid
    token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    db_token = RefreshToken(token=token, user_id=user_id, device_info=device_info, expiry=expiry)
    db.add(db_token)
    db.commit()
    return token


def verify_refresh_token(db: Session, token: str) -> Optional[User]:
    """Return the associated user if the refresh token is valid and not expired."""
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token).first()
    if not db_token or db_token.expiry < datetime.utcnow():
        return None
    return db_token.user


def get_user_roles(user: User) -> List[str]:
    """Return a list of role names assigned to a user."""
    return [role.name for role in user.roles]


def create_password_reset(db: Session, user_id: int) -> str:
    """Create a password reset token for the given user."""
    import uuid
    token = str(uuid.uuid4())
    expiry = datetime.utcnow() + timedelta(minutes=15)
    reset = PasswordReset(token=token, user_id=user_id, expiry=expiry)
    db.add(reset)
    db.commit()
    return token


def verify_password_reset(db: Session, token: str) -> Optional[PasswordReset]:
    """Return the PasswordReset entry if valid and not expired."""
    reset = db.query(PasswordReset).filter(PasswordReset.token == token).first()
    if not reset or reset.expiry < datetime.utcnow():
        return None
    return reset


def reset_user_password(db: Session, token: str, new_password: str) -> bool:
    """Update the user's password if the reset token is valid."""
    reset = verify_password_reset(db, token)
    if not reset:
        return False
    user = reset.user
    user.password_hash = hash_password(new_password)
    db.delete(reset)
    db.commit()
    return True


def decode_access_token(token: str) -> Optional[schemas.TokenData]:
    """Decode a JWT access token and return the contained data."""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        roles = payload.get("roles", [])
        if user_id is None:
            return None
        return schemas.TokenData(user_id=int(user_id), roles=list(roles))
    except JWTError:
        return None


def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
    """Update a user's password after verifying the old password."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not verify_password(old_password, user.password_hash):
        return False
    user.password_hash = hash_password(new_password)
    db.commit()
    return True
