"""
UniMap 3.0 - Health Check Tests
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestHealthEndpoints:
    async def test_health_returns_200(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data

    async def test_readiness_probe(self, client: AsyncClient):
        response = await client.get("/ready")
        # Will be degraded in test environment (no real DB/Redis)
        assert response.status_code in (200, 503)
        data = response.json()
        assert "status" in data
        assert "checks" in data

    async def test_docs_accessible(self, client: AsyncClient):
        response = await client.get("/api/v1/docs")
        assert response.status_code == 200

    async def test_openapi_json_accessible(self, client: AsyncClient):
        response = await client.get("/api/v1/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        # Verify key endpoints exist
        paths = data["paths"]
        assert "/api/v1/auth/login" in paths
        assert "/api/v1/maps" in paths
        assert "/api/v1/clinics" in paths
        assert "/api/v1/events" in paths
        assert "/api/v1/agenda" in paths
