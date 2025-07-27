"""
Entrypoint for the auth microservice.

Initialises the FastAPI application, sets up CORS and includes the
authentication routes.  On startup, database tables are created.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from .models.base import Base
from .api.routes_auth import router as auth_router


def init_db() -> None:
    """Create database tables on startup."""
    Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(title="Auth Service", version="0.1.0")

    # Allow cross‑origin requests in development; restrict origins via env
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    init_db()

    app.include_router(auth_router)

    return app


app = create_app()