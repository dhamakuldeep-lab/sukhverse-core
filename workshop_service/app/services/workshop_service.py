"""
Business logic for the workshop service.
"""

from sqlalchemy.orm import Session
from ..models.workshop import Workshop, Step, Substep, TrainerWorkshopMapping, StudentWorkshopProgress
from ..schemas.workshop import WorkshopCreate, StepCreate, SubstepCreate, ProgressUpdate
from ..events.producer import publish_event


def create_workshop(db: Session, workshop_in: WorkshopCreate, creator_user_id: int) -> Workshop:
    workshop = Workshop(
        title=workshop_in.title,
        description=workshop_in.description,
        creator_user_id=creator_user_id,
    )
    db.add(workshop)
    db.flush()  # assign ID before adding steps
    for step_data in workshop_in.steps:
        step = Step(
            workshop_id=workshop.id,
            title=step_data.title,
            step_type=step_data.step_type,
        )
        db.add(step)
        db.flush()
        for sub_data in step_data.substeps:
            sub = Substep(
                step_id=step.id,
                title=sub_data.title,
                substep_type=sub_data.substep_type,
                order_index=sub_data.order_index,
            )
            db.add(sub)
    db.commit()
    db.refresh(workshop)
    publish_event("workshop_created", {"workshop_id": workshop.id, "creator_user_id": creator_user_id})
    return workshop


def get_workshop(db: Session, workshop_id: int) -> Workshop | None:
    return db.query(Workshop).filter(Workshop.id == workshop_id).first()


def update_progress(db: Session, progress: ProgressUpdate) -> StudentWorkshopProgress:
    record = StudentWorkshopProgress(
        user_id=progress.user_id,
        workshop_id=progress.workshop_id,
        step_id=progress.step_id,
        substep_id=progress.substep_id,
        status=progress.status,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    publish_event(
        "step_completed" if progress.status == "completed" else "step_updated",
        {
            "user_id": progress.user_id,
            "workshop_id": progress.workshop_id,
            "step_id": progress.step_id,
            "substep_id": progress.substep_id,
            "status": progress.status,
        },
    )
    return record