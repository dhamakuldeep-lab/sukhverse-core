"""
Business logic for the quiz service.
"""

from sqlalchemy.orm import Session
from ..models.quiz import Quiz, Question, Option, StudentQuizAttempt, QuizResult
from ..schemas.quiz import QuizCreate, QuizAttemptCreate
from ..events.producer import publish_event


def create_quiz(db: Session, quiz_in: QuizCreate) -> Quiz:
    quiz = Quiz(title=quiz_in.title, linked_to=quiz_in.linked_to, duration=quiz_in.duration)
    db.add(quiz)
    db.flush()
    for q in quiz_in.questions:
        question = Question(quiz_id=quiz.id, content=q.content, type=q.type)
        db.add(question)
        db.flush()
        for opt in q.options:
            option = Option(question_id=question.id, label=opt.label, is_correct=opt.is_correct)
            db.add(option)
    db.commit()
    db.refresh(quiz)
    return quiz


def get_quiz(db: Session, quiz_id: int) -> Quiz | None:
    return db.query(Quiz).filter(Quiz.id == quiz_id).first()


def submit_quiz(db: Session, quiz_id: int, attempt_in: QuizAttemptCreate) -> QuizResult:
    # Persist the attempt
    attempt = StudentQuizAttempt(user_id=attempt_in.user_id, quiz_id=quiz_id, answers_json=attempt_in.answers)
    db.add(attempt)
    # Score the quiz
    quiz = get_quiz(db, quiz_id)
    if not quiz:
        raise ValueError("Quiz not found")
    total_questions = len(quiz.questions)
    correct = 0
    for question in quiz.questions:
        selected = attempt_in.answers.get(str(question.id))
        for option in question.options:
            if option.id == selected and option.is_correct:
                correct += 1
    score = int((correct / total_questions) * 100) if total_questions else 0
    pass_fail = score >= 50
    result = QuizResult(quiz_id=quiz_id, user_id=attempt_in.user_id, score=score, pass_fail=pass_fail, result_json={"correct": correct, "total": total_questions})
    db.add(result)
    db.commit()
    db.refresh(result)
    publish_event(
        "quiz_submitted",
        {
            "quiz_id": quiz_id,
            "user_id": attempt_in.user_id,
            "score": score,
            "pass_fail": pass_fail,
        },
    )
    return result