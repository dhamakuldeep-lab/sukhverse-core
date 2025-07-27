"""
Entrypoint for the workshop service.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models.base import Base
from .api.routes_workshop import router as workshop_router


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(title="Workshop Service", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    init_db()
    app.include_router(workshop_router)
    return app


app = create_app()