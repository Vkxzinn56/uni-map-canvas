"""
UniMap 3.0 - Test Configuration
Pytest fixtures with async SQLAlchemy + TestClient
"""
import asyncio
import uuid
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from backend.main import create_app
from backend.shared.database.engine import Base, get_db
from backend.shared.cache.redis_service import CacheService, get_cache
from backend.shared.security.jwt import password_service, token_service
from backend.shared.security.rbac import UserRole

# ─── Test Database ─────────────────────────────────────────────────────────────
TEST_DATABASE_URL = (
    "postgresql+asyncpg://unimap_test:unimap_test_pass@localhost:5432/unimap_test_db"
)

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionFactory = async_sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db():
    """Create all tables once per session."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Per-test DB session that rolls back after each test."""
    async with test_engine.connect() as conn:
        async with conn.begin() as trans:
            session = AsyncSession(bind=conn, expire_on_commit=False)
            yield session
            await trans.rollback()
            await session.close()


# ─── Mock Cache ────────────────────────────────────────────────────────────────
class MockCacheService:
    """In-memory cache mock for tests."""

    def __init__(self):
        self._store: dict[str, Any] = {}

    async def get(self, key: str) -> Any:
        return self._store.get(key)

    async def set(self, key: str, value: Any, ttl: int | None = None) -> None:
        self._store[key] = value

    async def delete(self, key: str) -> int:
        return 1 if self._store.pop(key, None) else 0

    async def exists(self, key: str) -> bool:
        return key in self._store

    async def delete_pattern(self, pattern: str) -> int:
        return 0

    async def incr(self, key: str, amount: int = 1) -> int:
        current = self._store.get(key, 0)
        self._store[key] = current + amount
        return self._store[key]

    async def health_check(self) -> bool:
        return True


@pytest.fixture
def mock_cache() -> MockCacheService:
    return MockCacheService()


# ─── App + Client ──────────────────────────────────────────────────────────────
@pytest.fixture
def app(db_session, mock_cache):
    app = create_app()

    async def override_db():
        yield db_session

    async def override_cache():
        yield mock_cache

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_cache] = override_cache
    return app


@pytest_asyncio.fixture
async def client(app) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


# ─── User Factories ────────────────────────────────────────────────────────────
def make_user_token(
    user_id: str | None = None,
    role: str = UserRole.STUDENT.value,
    extra: dict | None = None,
) -> str:
    uid = user_id or str(uuid.uuid4())
    return token_service.create_access_token(uid, role, extra)


@pytest.fixture
def visitor_token() -> str:
    return make_user_token(role=UserRole.VISITOR.value)


@pytest.fixture
def student_token() -> str:
    return make_user_token(role=UserRole.STUDENT.value)


@pytest.fixture
def professor_token() -> str:
    return make_user_token(role=UserRole.PROFESSOR.value)


@pytest.fixture
def coordinator_token() -> str:
    return make_user_token(role=UserRole.COORDINATOR.value)


@pytest.fixture
def admin_token() -> str:
    return make_user_token(role=UserRole.ADMIN.value)


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}
