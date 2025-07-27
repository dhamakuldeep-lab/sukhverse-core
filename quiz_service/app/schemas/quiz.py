"""
Pydantic models for the quiz service.
"""

from typing import List, Optional
from pydantic import BaseModel


class OptionCreate(BaseModel):
    label: str
    is_correct: bool


class QuestionCreate(BaseModel):
    content: str
    type: str
    options: List[OptionCreate]


class QuizCreate(BaseModel):
    title: str
    linked_to: Optional[str] = None
    duration: Optional[int] = None
    questions: List[QuestionCreate]


class OptionOut(OptionCreate):
    id: int

    class Config:
        orm_mode = True


class QuestionOut(BaseModel):
    id: int
    content: str
    type: str
    options: List[OptionOut]

    class Config:
        orm_mode = True


class QuizOut(BaseModel):
    id: int
    title: str
    linked_to: Optional[str]
    duration: Optional[int]
    questions: List[QuestionOut]

    class Config:
        orm_mode = True


class QuizAttemptCreate(BaseModel):
    user_id: int
    answers: dict  # mapping question_id to selected option id


class QuizResultOut(BaseModel):
    id: int
    quiz_id: int
    user_id: int
    score: int
    pass_fail: bool
    result_json: Optional[dict]

    class Config:
        orm_mode = True