"""
UniMap 3.0 - Redis Cache Service
Infrastructure: Cache Layer with TTL, invalidation, and prefix namespacing
"""
import json
from collections.abc import AsyncGenerator
from typing import Any

import redis.asyncio as aioredis

from backend.core.config.settings import settings


class CacheService:
    """Redis-backed async cache with namespace isolation."""

    PREFIX = "unimap:"

    def __init__(self, redis_client: aioredis.Redis) -> None:
        self._redis = redis_client

    def _key(self, key: str) -> str:
        return f"{self.PREFIX}{key}"

    async def get(self, key: str) -> Any | None:
        raw = await self._redis.get(self._key(key))
        if raw is None:
            return None
        return json.loads(raw)

    async def set(
        self,
        key: str,
        value: Any,
        ttl: int | None = None,
    ) -> None:
        ttl = ttl or settings.REDIS_CACHE_TTL
        serialized = json.dumps(value, default=str)
        await self._redis.setex(self._key(key), ttl, serialized)

    async def delete(self, key: str) -> int:
        return await self._redis.delete(self._key(key))

    async def delete_pattern(self, pattern: str) -> int:
        keys = await self._redis.keys(self._key(pattern))
        if not keys:
            return 0
        return await self._redis.delete(*keys)

    async def exists(self, key: str) -> bool:
        return bool(await self._redis.exists(self._key(key)))

    async def expire(self, key: str, ttl: int) -> bool:
        return bool(await self._redis.expire(self._key(key), ttl))

    async def incr(self, key: str, amount: int = 1) -> int:
        return await self._redis.incrby(self._key(key), amount)

    async def health_check(self) -> bool:
        try:
            await self._redis.ping()
            return True
        except Exception:
            return False


# ─── Pool singleton ────────────────────────────────────────────────────────────
_redis_pool: aioredis.Redis | None = None


async def get_redis_pool() -> aioredis.Redis:
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = aioredis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True,
            max_connections=50,
        )
    return _redis_pool


async def get_cache() -> AsyncGenerator[CacheService, None]:
    """FastAPI dependency."""
    pool = await get_redis_pool()
    yield CacheService(pool)
