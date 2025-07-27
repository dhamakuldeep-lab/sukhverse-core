"""
SQLAlchemy models for the quiz service.
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from .base import Base


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    linked_to = Column(String(100), nullable=True)  # external identifier (e.g., workshop_id)
    duration = Column(Integer, nullable=True)

    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    content = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # e.g. mcq, code

    quiz = relationship("Quiz", back_populates="questions")
    options = relationship("Option", back_populates="question", cascade="all, delete-orphan")


class Option(Base):
    __tablename__ = "options"
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    label = Column(String(200), nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship("Question", back_populates="options")


class StudentQuizAttempt(Base):
    __tablename__ = "student_quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    quiz_id = Column(Integer, nullable=False)
    started_at = Column(DateTime(timezone=False), server_default=func.now())
    completed_at = Column(DateTime(timezone=False), nullable=True)
    answers_json = Column(JSON, nullable=True)


class QuizResult(Base):
    __tablename__ = "quiz_results"
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    pass_fail = Column(Boolean, nullable=False)
    result_json = Column(JSON, nullable=True)