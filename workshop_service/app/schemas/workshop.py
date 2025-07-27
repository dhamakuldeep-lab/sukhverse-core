"""
Pydantic models for workshop API requests and responses.
"""

from typing import List, Optional
from pydantic import BaseModel


class SubstepCreate(BaseModel):
    title: str
    substep_type: str
    order_index: int


class StepCreate(BaseModel):
    title: str
    step_type: str
    substeps: List[SubstepCreate]


class WorkshopCreate(BaseModel):
    title: str
    description: Optional[str] = None
    steps: List[StepCreate]


class SubstepOut(SubstepCreate):
    id: int

    class Config:
        orm_mode = True


class StepOut(BaseModel):
    id: int
    title: str
    step_type: str
    substeps: List[SubstepOut]

    class Config:
        orm_mode = True


class WorkshopOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    steps: List[StepOut]

    class Config:
        orm_mode = True


class ProgressUpdate(BaseModel):
    user_id: int
    workshop_id: int
    step_id: int
    substep_id: int
    status: str