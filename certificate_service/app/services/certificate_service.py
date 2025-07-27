"""
Business logic for the certificate service.
"""

from pathlib import Path
from datetime import datetime
import json
import os
from sqlalchemy.orm import Session

from ..models.certificate import Certificate, CertificateTemplate, IssuedCertificate
from ..schemas.certificate import CertificateCreate, CertificateTemplateCreate, IssueCertificateRequest
from ..events.producer import publish_event


def create_certificate(db: Session, cert_in: CertificateCreate) -> Certificate:
    cert = Certificate(
        workshop_id=cert_in.workshop_id,
        name=cert_in.name,
        criteria=cert_in.criteria,
    )
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert


def create_template(db: Session, template_in: CertificateTemplateCreate) -> CertificateTemplate:
    tmpl = CertificateTemplate(
        format_json=template_in.format_json,
        preview_path=template_in.preview_path,
    )
    db.add(tmpl)
    db.commit()
    db.refresh(tmpl)
    return tmpl


def issue_certificate(db: Session, req: IssueCertificateRequest) -> IssuedCertificate:
    # In a real implementation, we would render a PDF using the template and upload it to object storage.
    filename = f"certificate-{req.certificate_id}-{req.user_id}-{int(datetime.utcnow().timestamp())}.pdf"
    file_url = f"/certificates/{filename}"  # pretend path
    issued = IssuedCertificate(
        certificate_id=req.certificate_id,
        user_id=req.user_id,
        file_url=file_url,
    )
    db.add(issued)
    db.commit()
    db.refresh(issued)
    publish_event("certificate_issued", {"certificate_id": req.certificate_id, "user_id": req.user_id, "file_url": file_url})
    return issued