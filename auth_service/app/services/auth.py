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
