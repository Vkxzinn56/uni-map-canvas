"""
UniMap 3.0 - Maps Integration Tests
Public endpoints should work without authentication
"""
import uuid

import pytest
from httpx import AsyncClient

MAPS_URL = "/api/v1/maps"


@pytest.mark.asyncio
class TestMapEndpoints:
    async def test_get_map_unauthenticated(self, client: AsyncClient):
        """Maps are publicly accessible — no token needed."""
        response = await client.get(MAPS_URL)
        assert response.status_code == 200
        data = response.json()
        assert "blocks" in data
        assert "total_blocks" in data
        assert "total_rooms" in data

    async def test_get_map_with_visitor_token(self, client: AsyncClient, visitor_token):
        response = await client.get(
            MAPS_URL, headers={"Authorization": f"Bearer {visitor_token}"}
        )
        assert response.status_code == 200

    async def test_get_blocks(self, client: AsyncClient):
        response = await client.get(f"{MAPS_URL}/blocks")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    async def test_get_blocks_filter_by_type(self, client: AsyncClient):
        response = await client.get(f"{MAPS_URL}/blocks?block_type=academic")
        assert response.status_code == 200

    async def test_get_nonexistent_block(self, client: AsyncClient):
        response = await client.get(f"{MAPS_URL}/blocks/NOTEXIST")
        assert response.status_code == 404

    async def test_route_endpoint(self, client: AsyncClient):
        response = await client.post(
            f"{MAPS_URL}/route",
            json={
                "origin_block_code": "BLOCO_A",
                "destination_block_code": "BLOCO_B",
                "accessibility": False,
            },
        )
        # Either found a route or 404 — both are valid for empty DB
        assert response.status_code in (200, 404)


@pytest.mark.asyncio
class TestMapAccessControl:
    """Verify that map data is accessible to all roles."""

    async def test_student_can_access_map(self, client: AsyncClient, student_token):
        response = await client.get(
            MAPS_URL, headers={"Authorization": f"Bearer {student_token}"}
        )
        assert response.status_code == 200

    async def test_admin_can_access_map(self, client: AsyncClient, admin_token):
        response = await client.get(
            MAPS_URL, headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
