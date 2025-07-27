"""
SQLAlchemy models for the certificate service.
"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func

from .base import Base


class Certificate(Base):
    __tablename__ = "certificates"
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    criteria = Column(JSON, nullable=True)


class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"
    id = Column(Integer, primary_key=True, index=True)
    format_json = Column(JSON, nullable=False)
    preview_path = Column(String(255), nullable=True)


class IssuedCertificate(Base):
    __tablename__ = "issued_certificates"
    id = Column(Integer, primary_key=True, index=True)
    certificate_id = Column(Integer, ForeignKey("certificates.id"), nullable=False)
    user_id = Column(Integer, nullable=False)
    issued_at = Column(DateTime(timezone=False), server_default=func.now())
    file_url = Column(String(255), nullable=True)