"""
Entrypoint for the quiz microservice.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models.base import Base
from .api.routes_quiz import router as quiz_router


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(title="Quiz Service", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_db()
    app.include_router(quiz_router)
    return app


app = create_app()