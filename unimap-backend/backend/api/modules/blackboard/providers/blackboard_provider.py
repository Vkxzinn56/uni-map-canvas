"""
UniMap 3.0 - Blackboard Provider
Integration: HTTP client + OAuth2 token management for Blackboard REST API

PREPARED — NOT ACTIVE. Activate with BLACKBOARD_ENABLED=true
"""
import time
from typing import Any

import httpx

from backend.core.config.settings import settings


class BlackboardTokenCache:
    """Simple in-memory token cache (TTL-aware)."""

    def __init__(self) -> None:
        self._token: str | None = None
        self._expires_at: float = 0.0

    def get(self) -> str | None:
        if self._token and time.time() < self._expires_at - 30:
            return self._token
        return None

    def set(self, token: str, expires_in: int) -> None:
        self._token = token
        self._expires_at = time.time() + expires_in

    def clear(self) -> None:
        self._token = None
        self._expires_at = 0.0


class BlackboardProvider:
    """
    Blackboard REST API v3 HTTP provider.
    Handles OAuth2 client credentials flow and request routing.

    Reference: https://developer.blackboard.com/portal/displayApi
    """

    _token_cache = BlackboardTokenCache()

    def __init__(self) -> None:
        self._base_url = settings.BLACKBOARD_BASE_URL
        self._client_id = settings.BLACKBOARD_CLIENT_ID
        self._client_secret = settings.BLACKBOARD_CLIENT_SECRET

    async def _get_token(self) -> str:
        cached = self._token_cache.get()
        if cached:
            return cached

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}/learn/api/public/v1/oauth2/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=10.0,
            )
            response.raise_for_status()
            data = response.json()
            token = data["access_token"]
            expires_in = data.get("expires_in", 3600)
            self._token_cache.set(token, expires_in)
            return token

    async def get(self, path: str, params: dict | None = None) -> Any:
        """Authenticated GET request."""
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self._base_url}{path}",
                params=params,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Accept": "application/json",
                },
                timeout=15.0,
            )
            response.raise_for_status()
            return response.json()

    async def post(self, path: str, body: dict) -> Any:
        """Authenticated POST request."""
        token = await self._get_token()
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self._base_url}{path}",
                json=body,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=15.0,
            )
            response.raise_for_status()
            return response.json()

    # ─── Blackboard REST Endpoints ────────────────────────────────────────────

    async def get_user(self, username: str) -> dict:
        return await self.get(
            f"/learn/api/public/v1/users",
            params={"userName": username},
        )

    async def get_memberships(self, user_id: str) -> dict:
        return await self.get(
            f"/learn/api/public/v1/users/{user_id}/courses",
        )

    async def get_grades(self, course_id: str, user_id: str) -> dict:
        return await self.get(
            f"/learn/api/public/v2/courses/{course_id}/gradebook/users/{user_id}",
        )

    async def get_announcements(self, course_id: str) -> dict:
        return await self.get(
            f"/learn/api/public/v1/courses/{course_id}/announcements",
        )

    async def ping(self) -> bool:
        try:
            await self.get("/learn/api/public/v1/system/version")
            return True
        except Exception:
            return False
