"""
Client for interacting with the auth service via REST.

The user management service uses this client to fetch user identity
information (email, roles) and to assign roles to users.  In a
production system you may wish to use service discovery and handle
authentication between services.
"""

import os
from typing import Any, Dict

import httpx


AUTH_API_URL = os.getenv("AUTH_API_URL", "http://localhost:8000/auth")


async def get_user(user_id: int) -> Dict[str, Any]:
    async with httpx.AsyncClient(base_url=AUTH_API_URL) as client:
        resp = await client.get(f"/users/{user_id}")
        resp.raise_for_status()
        return resp.json()


async def assign_role(user_id: int, role_id: int) -> None:
    async with httpx.AsyncClient(base_url=AUTH_API_URL) as client:
        resp = await client.post(f"/roles/assign", json={"user_id": user_id, "role_id": role_id})
        resp.raise_for_status()