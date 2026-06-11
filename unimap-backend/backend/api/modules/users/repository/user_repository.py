"""
UniMap 3.0 - User Repository
Repository Pattern: Data access for User aggregate
"""
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.users.models.user import User
from backend.shared.database.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def find_by_email(self, email: str) -> User | None:
        stmt = select(User).where(
            User.email == email.lower(),
            User.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_cpf_hash(self, cpf_hash: str) -> User | None:
        stmt = select(User).where(
            User.cpf_hash == cpf_hash,
            User.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_role(self, role: str, skip: int = 0, limit: int = 100) -> list[User]:
        stmt = (
            select(User)
            .where(User.role == role, User.deleted_at.is_(None))
            .offset(skip)
            .limit(limit)
            .order_by(User.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def anonymize(self, user_id: uuid.UUID) -> bool:
        """LGPD: Anonymize user's personal data while preserving audit trail."""
        from datetime import datetime, timezone

        user = await self.find_by_id(user_id)
        if not user:
            return False

        user.email = f"anonymized_{str(user_id)[:8]}@anonymized.local"
        user.full_name = "Anonymized User"
        user.display_name = None
        user.avatar_url = None
        user.phone = None
        user.cpf_encrypted = None
        user.cpf_hash = None
        user.address_encrypted = None
        user.last_login_ip = None
        user.lgpd_consent_ip = None
        user.anonymized_at = datetime.now(timezone.utc)

        await self._session.flush()
        return True
