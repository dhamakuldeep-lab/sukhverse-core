"""
API routes for certificate management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.certificate import CertificateCreate, CertificateOut, CertificateTemplateCreate, IssueCertificateRequest, IssuedCertificateOut
from ..models.certificate import Certificate, IssuedCertificate
from ..services import certificate_service

router = APIRouter(prefix="/certificates", tags=["certificates"])


@router.post("", response_model=CertificateOut, status_code=status.HTTP_201_CREATED)
def create_certificate_route(cert_in: CertificateCreate, db: Session = Depends(get_db)):
    cert = certificate_service.create_certificate(db, cert_in)
    return cert


@router.post("/templates", status_code=status.HTTP_201_CREATED)
def create_template_route(tmpl_in: CertificateTemplateCreate, db: Session = Depends(get_db)):
    tmpl = certificate_service.create_template(db, tmpl_in)
    return {"template_id": tmpl.id}


@router.post("/issue", response_model=IssuedCertificateOut, status_code=status.HTTP_201_CREATED)
def issue_certificate_route(req: IssueCertificateRequest, db: Session = Depends(get_db)):
    issued = certificate_service.issue_certificate(db, req)
    return issued


@router.get("/user/{user_id}", response_model=list[IssuedCertificateOut])
def list_user_certificates(user_id: int, db: Session = Depends(get_db)):
    certs = db.query(IssuedCertificate).filter(IssuedCertificate.user_id == user_id).all()
    return certs