"""
UniMap 3.0 - Clinics Integration Tests
"""
import pytest
from httpx import AsyncClient

CLINICS_URL = "/api/v1/clinics"


@pytest.mark.asyncio
class TestClinicsPublicAccess:
    async def test_list_clinics_unauthenticated(self, client: AsyncClient):
        """Clinic listing is public."""
        response = await client.get(CLINICS_URL)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_list_clinics_visitor(self, client: AsyncClient, visitor_token):
        response = await client.get(
            CLINICS_URL, headers={"Authorization": f"Bearer {visitor_token}"}
        )
        assert response.status_code == 200

    async def test_filter_by_type(self, client: AsyncClient):
        response = await client.get(f"{CLINICS_URL}?clinic_type=dental")
        assert response.status_code == 200

    async def test_get_nonexistent_clinic(self, client: AsyncClient):
        import uuid
        fake_id = uuid.uuid4()
        response = await client.get(f"{CLINICS_URL}/{fake_id}")
        assert response.status_code == 404


@pytest.mark.asyncio
class TestClinicsAppointments:
    async def test_visitor_cannot_book(self, client: AsyncClient, visitor_token):
        """VISITOR must be blocked from booking."""
        import uuid
        response = await client.post(
            f"{CLINICS_URL}/appointments",
            json={
                "clinic_id": str(uuid.uuid4()),
                "scheduled_at": "2025-12-01T09:00:00Z",
                "appointment_type": "consultation",
            },
            headers={"Authorization": f"Bearer {visitor_token}"},
        )
        assert response.status_code == 403

    async def test_unauthenticated_cannot_book(self, client: AsyncClient):
        import uuid
        response = await client.post(
            f"{CLINICS_URL}/appointments",
            json={
                "clinic_id": str(uuid.uuid4()),
                "scheduled_at": "2025-12-01T09:00:00Z",
            },
        )
        assert response.status_code == 401

    async def test_student_can_view_own_appointments(
        self, client: AsyncClient, student_token
    ):
        response = await client.get(
            f"{CLINICS_URL}/appointments/me",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_visitor_cannot_view_appointments(
        self, client: AsyncClient, visitor_token
    ):
        response = await client.get(
            f"{CLINICS_URL}/appointments/me",
            headers={"Authorization": f"Bearer {visitor_token}"},
        )
        assert response.status_code == 403

    async def test_student_can_view_own_budgets(
        self, client: AsyncClient, student_token
    ):
        response = await client.get(
            f"{CLINICS_URL}/budgets/me",
            headers={"Authorization": f"Bearer {student_token}"},
        )
        assert response.status_code == 200
