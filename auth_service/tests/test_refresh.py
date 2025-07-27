import os
import sys
import pathlib
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Use SQLite for tests
DB_PATH = "test_auth.db"
os.environ["DATABASE_URL"] = f"sqlite:///{DB_PATH}"

# Ensure service package is importable
sys.path.append(str(pathlib.Path(__file__).resolve().parents[2]))

from auth_service.app.main import create_app
from auth_service.app.database import SessionLocal
from auth_service.app.models.user import RefreshToken

@pytest.fixture(scope="module")
def client():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    app = create_app()
    with TestClient(app) as c:
        yield c
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

@pytest.fixture(autouse=True)
def mock_publish_event():
    with patch("auth_service.app.services.auth.publish_event") as mock:
        yield mock

def test_refresh_token_flow(client):
    email = "user@example.com"
    password = "strongpassword"

    resp = client.post("/auth/register", json={"email": email, "password": password})
    assert resp.status_code == 201

    resp = client.post("/auth/login", data={"username": email, "password": password})
    assert resp.status_code == 200
    tokens = resp.json()
    refresh_token = tokens.get("refresh_token")
    assert refresh_token

    # Verify refresh token persisted
    with SessionLocal() as db:
        assert db.query(RefreshToken).filter(RefreshToken.token == refresh_token).first()

    resp = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert resp.status_code == 200
    new_tokens = resp.json()
    assert new_tokens["refresh_token"] == refresh_token
    assert new_tokens["access_token"]
    assert new_tokens["token_type"] == "bearer"
