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


def test_me_requires_auth_and_returns_user(client):
    """Verify /auth/me requires authentication and returns the current user."""

    # Unauthenticated request should be rejected
    resp = client.get("/auth/me")
    assert resp.status_code == 401

    # Register and login to obtain a valid token
    reg = client.post(
        "/auth/register",
        json={"email": "me@example.com", "password": "pass1234"},
    )
    user_id = reg.json()["id"]

    login = client.post(
        "/auth/login",
        data={"username": "me@example.com", "password": "pass1234"},
    )
    assert login.status_code == 200
    token = login.json()["access_token"]

    # JWT should decode to the correct user id
    from auth_service.app.services.auth import decode_access_token

    payload = decode_access_token(token)
    assert payload and payload.user_id == user_id

    # Authenticated call should return the user details
    resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == user_id
    assert data["email"] == "me@example.com"


def test_forgot_and_reset_missing(client):
    resp1 = client.post("/auth/forgot-password", json={"email": "a@b.com"})
    resp2 = client.post(
        "/auth/reset-password",
        json={"token": "t", "new_password": "newpass123"},
    )
    assert resp1.status_code == 404
    assert resp2.status_code == 400

