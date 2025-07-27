"""
SQLAlchemy models for the workshop service.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class Workshop(Base):
    __tablename__ = "workshops"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    creator_user_id = Column(Integer, nullable=False)
    published_flag = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    steps = relationship("Step", back_populates="workshop", cascade="all, delete-orphan")
    trainers = relationship("TrainerWorkshopMapping", back_populates="workshop", cascade="all, delete-orphan")


class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True, index=True)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)
    title = Column(String(200), nullable=False)
    step_type = Column(String(50), nullable=False)  # intro, theory, code, quiz, certificate

    workshop = relationship("Workshop", back_populates="steps")
    substeps = relationship("Substep", back_populates="step", cascade="all, delete-orphan")


class Substep(Base):
    __tablename__ = "substeps"
    id = Column(Integer, primary_key=True, index=True)
    step_id = Column(Integer, ForeignKey("steps.id"), nullable=False)
    title = Column(String(200), nullable=False)
    substep_type = Column(String(50), nullable=False)  # content, quiz, code
    order_index = Column(Integer, nullable=False)

    step = relationship("Step", back_populates="substeps")


class TrainerWorkshopMapping(Base):
    __tablename__ = "trainer_workshop_mapping"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id"), nullable=False)

    workshop = relationship("Workshop", back_populates="trainers")


class StudentWorkshopProgress(Base):
    __tablename__ = "student_workshop_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    workshop_id = Column(Integer, nullable=False)
    step_id = Column(Integer, nullable=False)
    substep_id = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="in_progress")  # in_progress, completed
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())