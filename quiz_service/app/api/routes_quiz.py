"""
API routes for the quiz service.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.quiz import QuizCreate, QuizOut, QuizAttemptCreate, QuizResultOut
from ..services import quiz_service

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("", response_model=QuizOut, status_code=status.HTTP_201_CREATED)
def create_quiz_route(quiz_in: QuizCreate, db: Session = Depends(get_db)):
    quiz = quiz_service.create_quiz(db, quiz_in)
    return quiz


@router.get("/{quiz_id}", response_model=QuizOut)
def get_quiz_route(quiz_id: int, db: Session = Depends(get_db)):
    quiz = quiz_service.get_quiz(db, quiz_id)
    if not quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz not found")
    return quiz


@router.post("/{quiz_id}/attempts", response_model=QuizResultOut, status_code=status.HTTP_201_CREATED)
def submit_quiz_route(quiz_id: int, attempt_in: QuizAttemptCreate, db: Session = Depends(get_db)):
    try:
        result = quiz_service.submit_quiz(db, quiz_id, attempt_in)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return result