import pytest


def test_register_success(client):
    resp = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "user@example.com"
    assert "id" in data
    # kafka event mocked
    assert client.event_calls and client.event_calls[0]["topic"] == "user_registered"


def test_register_duplicate(client):
    client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "password123"},
    )
    resp = client.post(
        "/auth/register",
        json={"email": "dup@example.com", "password": "password123"},
    )
    assert resp.status_code == 400


def test_login_and_refresh(client):
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "secret123"},
    )
    resp = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "secret123"},
    )
    assert resp.status_code == 200
    token = resp.json()
    assert token["access_token"]
    assert token["refresh_token"]

    refresh_resp = client.post(
        "/auth/refresh",
        json={"refresh_token": token["refresh_token"]},
    )
    assert refresh_resp.status_code == 200
    refreshed = refresh_resp.json()
    assert refreshed["access_token"]
    assert refreshed["refresh_token"] == token["refresh_token"]


def test_me_not_implemented(client):
    resp = client.get("/auth/me")
    # dependency is missing, so FastAPI returns 422
    assert resp.status_code == 422


def test_forgot_and_reset_missing(client):
    resp1 = client.post("/auth/forgot-password", json={"email": "a@b.com"})
    resp2 = client.post(
        "/auth/reset-password",
        json={"token": "t", "password": "newpass123"},
    )
    assert resp1.status_code == 404
    assert resp2.status_code == 404

