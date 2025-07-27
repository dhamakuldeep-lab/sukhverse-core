"""
Database utilities for the auth service.

This module defines a SQLAlchemy engine and sessionmaker based on the
`DATABASE_URL` environment variable.  All services should create and
dispose sessions through `SessionLocal` to ensure proper connection
handling.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Pull the database URL from the environment.  When running under
# Docker Compose, the hostname corresponds to the postgres service name.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/auth_db")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI routes to get a database session.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()