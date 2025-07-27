import os
import sys
import pathlib
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch

# Use SQLite for tests
DB_PATH = '/tmp/test_auth_testcase.db'
os.environ['DATABASE_URL'] = f'sqlite:///{DB_PATH}'

# Ensure service package is importable
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from auth_service.app.main import create_app

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


def test_registration_success(client):
    payload = {
        "username": "kuldeep_test",
        "email": "kuldeep@example.com",
        "password": "StrongPass123",
        "roles": ["student"],
    }
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data.get("token_type") == "bearer"
    # Optional JWT role decoding
    # from auth_service.app.services.auth import decode_access_token
    # assert "student" in decode_access_token(data["access_token"]).roles
