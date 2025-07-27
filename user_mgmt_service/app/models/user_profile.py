"""
SQLAlchemy models for the user management microservice.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    user_id = Column(Integer, primary_key=True)
    bio = Column(String(255), nullable=True)
    contact_number = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    created_by = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())


class BulkUploadLog(Base):
    __tablename__ = "bulk_upload_logs"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    uploader_user_id = Column(Integer, nullable=False)
    status = Column(String(50), nullable=False, default="pending")
    timestamp = Column(DateTime(timezone=False), server_default=func.now())


class UserRoleAssignment(Base):
    __tablename__ = "user_role_assignments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    role_id = Column(Integer, nullable=False)
    assigned_by = Column(Integer, nullable=False)
    assigned_at = Column(DateTime(timezone=False), server_default=func.now())