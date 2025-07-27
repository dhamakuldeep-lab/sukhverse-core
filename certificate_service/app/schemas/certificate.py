"""
Pydantic models for the certificate service.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class CertificateCreate(BaseModel):
    workshop_id: int
    name: str
    criteria: Optional[Dict[str, Any]] = None


class CertificateTemplateCreate(BaseModel):
    format_json: Dict[str, Any]
    preview_path: Optional[str] = None


class IssueCertificateRequest(BaseModel):
    certificate_id: int
    user_id: int


class CertificateOut(BaseModel):
    id: int
    workshop_id: int
    name: str
    criteria: Optional[Dict[str, Any]]

    class Config:
        orm_mode = True


class IssuedCertificateOut(BaseModel):
    id: int
    certificate_id: int
    user_id: int
    issued_at: str
    file_url: Optional[str]

    class Config:
        orm_mode = True