"""
Business logic for authentication and user management in the auth service.
"""

from datetime import datetime, timedelta
from typing import List, Optional

from jose import JWTError, jwt
from sqlalchemy.orm import Session

from .. import schemas
from ..models.user import User, RefreshToken, Role
from ..utils.security import hash_password, verify_password
from ..events.producer import publish_event

import os


JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supersecretkey")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
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


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    to_encode = data.copy()
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
