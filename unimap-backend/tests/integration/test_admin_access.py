"""
UniMap 3.0 - Admin Access Control Tests
Verifies role enforcement on sensitive admin routes
"""
import uuid

import pytest
from httpx import AsyncClient

USERS_URL = "/api/v1/users"
AUDIT_URL = "/api/v1/audit"
ANALYTICS_URL = "/api/v1/analytics"


@pytest.mark.asyncio
class TestAdminEndpoints:
    async def test_visitor_cannot_list_users(self, client: AsyncClient, visitor_token):
        response = await client.get(
            USERS_URL, headers={"Authorization": f"Bearer {visitor_token}"}
        )
        assert response.status_code == 403

    async def test_student_cannot_list_users(self, client: AsyncClient, student_token):
        response = await client.get(
            USERS_URL, headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 403

    async def test_professor_cannot_list_users(
        self, client: AsyncClient, professor_token
    ):
        response = await client.get(
            USERS_URL, headers={"Authorization": f"Bearer {professor_token}"}
        )
        assert response.status_code == 403

    async def test_admin_can_list_users(self, client: AsyncClient, admin_token):
        response = await client.get(
            USERS_URL, headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "total" in data
        assert "items" in data

    async def test_admin_can_view_audit_logs(self, client: AsyncClient, admin_token):
        response = await client.get(
            f"{AUDIT_URL}/logs", headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200

    async def test_student_cannot_view_audit_logs(
        self, client: AsyncClient, student_token
    ):
        response = await client.get(
            f"{AUDIT_URL}/logs",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 403

    async def test_coordinator_can_view_analytics(
        self, client: AsyncClient, coordinator_token
    ):
        response = await client.get(
            f"{ANALYTICS_URL}/overview",
            headers={"Authorization": f"Bearer {coordinator_token}"},
        )
        assert response.status_code == 200

    async def test_student_cannot_view_analytics(
        self, client: AsyncClient, student_token
    ):
        response = await client.get(
            f"{ANALYTICS_URL}/overview",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 403


@pytest.mark.asyncio
class TestUserProfile:
    async def test_get_my_profile(self, client: AsyncClient, student_token):
        response = await client.get(
            f"{USERS_URL}/me",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code in (200, 404)

    async def test_unauthenticated_cannot_get_profile(self, client: AsyncClient):
        response = await client.get(f"{USERS_URL}/me")
        assert response.status_code == 401
