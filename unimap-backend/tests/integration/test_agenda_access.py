"""
UniMap 3.0 - Agenda Access Control Tests
VISITOR must be BLOCKED from agenda endpoints
"""
import pytest
from httpx import AsyncClient

AGENDA_URL = "/api/v1/agenda"


@pytest.mark.asyncio
class TestAgendaAccessControl:
    async def test_visitor_cannot_access_agenda(self, client: AsyncClient, visitor_token):
        """VISITOR must receive 403."""
        response = await client.get(
            AGENDA_URL, headers={"Authorization": f"Bearer {visitor_token}"}
        )
        assert response.status_code == 403

    async def test_unauthenticated_cannot_access_agenda(self, client: AsyncClient):
        """No token → 401."""
        response = await client.get(AGENDA_URL)
        assert response.status_code == 401

    async def test_student_can_access_agenda(self, client: AsyncClient, student_token):
        """Students get through (may get 404 if no profile, not 401/403)."""
        response = await client.get(
            AGENDA_URL, headers={"Authorization": f"Bearer {student_token}"}
        )
        # 404 = no student profile (expected in test DB) — not a permission issue
        assert response.status_code in (200, 404)

    async def test_professor_can_access_agenda(self, client: AsyncClient, professor_token):
        response = await client.get(
            AGENDA_URL, headers={"Authorization": f"Bearer {professor_token}"}
        )
        assert response.status_code in (200, 404)

    async def test_visitor_cannot_access_classes(self, client: AsyncClient, visitor_token):
        response = await client.get(
            f"{AGENDA_URL}/classes",
            headers={"Authorization": f"Bearer {visitor_token}"},
        )
        assert response.status_code == 403

    async def test_visitor_cannot_access_activities(self, client: AsyncClient, visitor_token):
        response = await client.get(
            f"{AGENDA_URL}/activities",
            headers={"Authorization": f"Bearer {visitor_token}"},
        )
        assert response.status_code == 403

    async def test_admin_can_access_agenda(self, client: AsyncClient, admin_token):
        response = await client.get(
            AGENDA_URL, headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code in (200, 404)
