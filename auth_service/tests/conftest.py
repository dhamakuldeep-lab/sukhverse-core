import sys
from types import SimpleNamespace
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

@pytest.fixture()
def client(monkeypatch):
    # Stub kafka module before importing app code
    class DummyProducer:
        def __init__(self, *args, **kwargs):
            pass

        def send(self, *args, **kwargs):
            pass

    sys.modules.setdefault("kafka", SimpleNamespace(KafkaProducer=DummyProducer))

    from auth_service.app import database as database_module
    from auth_service.app.models.base import Base

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    database_module.engine = engine
    database_module.SessionLocal = TestingSessionLocal

    from auth_service.app import schemas as schemas_pkg
    from auth_service.app.schemas import auth as auth_schemas

    # Expose schema classes at package level as expected by service code
    for name in (
        "UserCreate",
        "UserLogin",
        "UserOut",
        "Token",
        "RefreshTokenRequest",
    ):
        setattr(schemas_pkg, name, getattr(auth_schemas, name))

    from auth_service.app.main import create_app
    from auth_service.app.database import get_db
    from auth_service.app.events import producer as producer_module
    from auth_service.app import services
    from auth_service.app.services import auth as auth_service_module

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    events = []

    def fake_publish_event(topic, message, key=None):
        events.append({"topic": topic, "message": message, "key": key})

    monkeypatch.setattr(producer_module, "publish_event", fake_publish_event)
    monkeypatch.setattr(auth_service_module, "publish_event", fake_publish_event)

    # Override DB engine and session in the database module used by the app
    from auth_service.app import database as database_module
    database_module.engine = engine
    database_module.SessionLocal = TestingSessionLocal

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        c.event_calls = events
        yield c
