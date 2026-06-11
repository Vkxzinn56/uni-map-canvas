"""
UniMap 3.0 - Auth Integration Tests
Tests the full HTTP request/response cycle
"""
import pytest
from httpx import AsyncClient


REGISTER_URL = "/api/v1/auth/register"
LOGIN_URL = "/api/v1/auth/login"
REFRESH_URL = "/api/v1/auth/refresh"
LOGOUT_URL = "/api/v1/auth/logout"
ME_URL = "/api/v1/auth/me"

VALID_USER = {
    "email": "student@unimap.edu.br",
    "password": "StrongPass123!",
    "full_name": "Test Student",
    "lgpd_consent": True,
}


@pytest.mark.asyncio
class TestAuthEndpoints:
    async def test_register_success(self, client: AsyncClient):
        response = await client.post(REGISTER_URL, json=VALID_USER)
        assert response.status_code == 201
        data = response.json()
        assert "tokens" in data
        assert "user" in data
        assert data["user"]["email"] == VALID_USER["email"]
        assert data["user"]["role"] == "visitor"
        assert "access_token" in data["tokens"]
        assert "refresh_token" in data["tokens"]

    async def test_register_duplicate_email(self, client: AsyncClient):
        await client.post(REGISTER_URL, json=VALID_USER)
        response = await client.post(REGISTER_URL, json=VALID_USER)
        assert response.status_code == 409
        assert response.json()["error"]["code"] == "ALREADY_EXISTS"

    async def test_register_no_lgpd_consent(self, client: AsyncClient):
        payload = {**VALID_USER, "email": "other@test.com", "lgpd_consent": False}
        response = await client.post(REGISTER_URL, json=payload)
        assert response.status_code == 422

    async def test_register_weak_password(self, client: AsyncClient):
        payload = {**VALID_USER, "email": "weak@test.com", "password": "weak"}
        response = await client.post(REGISTER_URL, json=payload)
        assert response.status_code == 422

    async def test_login_success(self, client: AsyncClient):
        # Register first
        await client.post(REGISTER_URL, json={**VALID_USER, "email": "login_test@test.com"})
        response = await client.post(
            LOGIN_URL,
            json={"email": "login_test@test.com", "password": VALID_USER["password"]},
        )
        assert response.status_code == 200
        data = response.json()
        assert "tokens" in data
        assert data["tokens"]["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient):
        await client.post(REGISTER_URL, json={**VALID_USER, "email": "wrong@test.com"})
        response = await client.post(
            LOGIN_URL,
            json={"email": "wrong@test.com", "password": "WrongPass123!"},
        )
        assert response.status_code == 401
        assert response.json()["error"]["code"] == "INVALID_CREDENTIALS"

    async def test_login_nonexistent_email(self, client: AsyncClient):
        response = await client.post(
            LOGIN_URL,
            json={"email": "ghost@test.com", "password": "AnyPass123!"},
        )
        assert response.status_code == 401

    async def test_get_me_authenticated(self, client: AsyncClient, student_token):
        response = await client.get(
            ME_URL, headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert data["role"] == "student"

    async def test_get_me_no_token(self, client: AsyncClient):
        response = await client.get(ME_URL)
        assert response.status_code == 401

    async def test_refresh_tokens(self, client: AsyncClient):
        reg = await client.post(
            REGISTER_URL, json={**VALID_USER, "email": "refresh@test.com"}
        )
        refresh_token = reg.json()["tokens"]["refresh_token"]
        response = await client.post(
            REFRESH_URL, json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        # New tokens should differ from originals
        assert data["refresh_token"] != refresh_token

    async def test_logout(self, client: AsyncClient, student_token):
        response = await client.post(
            LOGOUT_URL, headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 204
