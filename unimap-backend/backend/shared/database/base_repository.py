"""
UniMap 3.0 - Generic Repository
Clean Architecture: Repository Pattern (Interface + Base Implementation)
"""
import uuid
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.shared.database.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class IRepository(ABC, Generic[T]):
    """Repository interface — DDD port."""

    @abstractmethod
    async def find_by_id(self, entity_id: uuid.UUID) -> T | None: ...

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> list[T]: ...

    @abstractmethod
    async def save(self, entity: T) -> T: ...

    @abstractmethod
    async def delete(self, entity_id: uuid.UUID) -> bool: ...


class BaseRepository(IRepository[T], Generic[T]):
    """Concrete async SQLAlchemy repository."""

    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        self._session = session
        self._model = model

    async def find_by_id(self, entity_id: uuid.UUID) -> T | None:
        stmt = select(self._model).where(
            self._model.id == entity_id,
            self._model.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_all(self, skip: int = 0, limit: int = 100) -> list[T]:
        stmt = (
            select(self._model)
            .where(self._model.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(self._model.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        stmt = select(func.count()).select_from(self._model).where(
            self._model.deleted_at.is_(None)
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()

    async def save(self, entity: T) -> T:
        self._session.add(entity)
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def save_many(self, entities: list[T]) -> list[T]:
        self._session.add_all(entities)
        await self._session.flush()
        return entities

    async def delete(self, entity_id: uuid.UUID) -> bool:
        """Hard delete."""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return False
        await self._session.delete(entity)
        await self._session.flush()
        return True

    async def soft_delete(self, entity_id: uuid.UUID) -> bool:
        """Soft delete — preserves history (LGPD compliant)."""
        entity = await self.find_by_id(entity_id)
        if not entity:
            return False
        entity.soft_delete()
        await self._session.flush()
        return True
