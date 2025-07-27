"""
Base class for SQLAlchemy models.

All models in this service should inherit from `Base` defined here.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()