"""
API routes for workshop management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.workshop import WorkshopCreate, WorkshopOut, ProgressUpdate
from ..services import workshop_service

router = APIRouter(prefix="/workshops", tags=["workshops"])


@router.post("", response_model=WorkshopOut, status_code=status.HTTP_201_CREATED)
def create_workshop_route(workshop_in: WorkshopCreate, db: Session = Depends(get_db)):
    # TODO: Determine creator_user_id from auth token
    creator_user_id = 1
    workshop = workshop_service.create_workshop(db, workshop_in, creator_user_id)
    return workshop


@router.get("/{workshop_id}", response_model=WorkshopOut)
def get_workshop_route(workshop_id: int, db: Session = Depends(get_db)):
    workshop = workshop_service.get_workshop(db, workshop_id)
    if not workshop:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workshop not found")
    return workshop


@router.post("/progress", status_code=status.HTTP_201_CREATED)
def update_progress_route(progress: ProgressUpdate, db: Session = Depends(get_db)):
    record = workshop_service.update_progress(db, progress)
    return {"message": "Progress recorded", "progress_id": record.id}