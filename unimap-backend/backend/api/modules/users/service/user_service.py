"""
UniMap 3.0 - Users Service
Application Layer: Profile and account management
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.users.models.user import User
from backend.api.modules.users.repository.user_repository import UserRepository
from backend.api.modules.students.models.student import Student
from backend.shared.exceptions.auth import (
    AlreadyExistsException,
    BusinessRuleException,
    NotFoundException,
    ValidationException,
)
from backend.shared.security.rbac import UserRole


class UserService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repo = UserRepository(session)

    async def get_profile(self, user_id: str) -> dict:
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)
        return self._serialize(user)

    async def update_profile(self, user_id: str, data: dict) -> dict:
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)

        allowed = ("full_name", "display_name", "phone", "avatar_url")
        for field in allowed:
            if field in data:
                setattr(user, field, data[field])

        # Handle CPF update with encryption
        if "cpf" in data and data["cpf"]:
            from backend.shared.security.encryption import encryption_service
            user.cpf_encrypted = encryption_service.encrypt(data["cpf"])
            user.cpf_hash = encryption_service.hash_sensitive(data["cpf"])

        # Handle address update with encryption
        if "address" in data and data["address"]:
            from backend.shared.security.encryption import encryption_service
            import json
            addr = json.dumps(data["address"]) if isinstance(data["address"], dict) else data["address"]
            user.address_encrypted = encryption_service.encrypt(addr)

        await self._repo.save(user)
        return self._serialize(user)

    async def request_deletion(self, user_id: str) -> None:
        """LGPD: Soft delete + anonymize personal data."""
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)
        await self._repo.anonymize(uuid.UUID(user_id))
        await self._repo.soft_delete(uuid.UUID(user_id))

    async def list_users(
        self,
        role: str | None = None,
        is_active: bool | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> dict:
        from sqlalchemy import func

        stmt = select(User).where(User.deleted_at.is_(None))
        if role:
            stmt = stmt.where(User.role == role)
        if is_active is not None:
            stmt = stmt.where(User.is_active == is_active)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        count_result = await self._session.execute(count_stmt)
        total = count_result.scalar_one()

        stmt = stmt.offset(skip).limit(limit).order_by(User.created_at.desc())
        result = await self._session.execute(stmt)
        users = result.scalars().all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [self._serialize(u) for u in users],
        }

    async def change_role(self, user_id: str, new_role: str) -> dict:
        try:
            role = UserRole(new_role)
        except ValueError:
            raise ValidationException(f"Invalid role: {new_role}")

        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)

        user.role = role.value
        await self._repo.save(user)
        return {"user_id": user_id, "role": user.role}

    async def block_user(self, user_id: str, reason: str) -> dict:
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)
        user.block(reason)
        await self._repo.save(user)
        return {"blocked": True, "reason": reason}

    async def unblock_user(self, user_id: str) -> dict:
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)
        user.unblock()
        await self._repo.save(user)
        return {"blocked": False}

    async def graduate_student(self, user_id: str) -> dict:
        """
        Transition STUDENT → ALUMNI.
        Preserves all history, blocks academic write access.
        """
        user = await self._repo.find_by_id(uuid.UUID(user_id))
        if not user:
            raise NotFoundException("User", user_id)
        if user.role != UserRole.STUDENT.value:
            raise BusinessRuleException("Only STUDENT accounts can be graduated")

        # Update student profile
        stmt = select(Student).where(
            Student.user_id == uuid.UUID(user_id),
            Student.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        student = result.scalar_one_or_none()
        if student:
            from datetime import date
            student.enrollment_status = "graduated"
            student.graduation_date = date.today()

        user.role = UserRole.ALUMNI.value
        await self._repo.save(user)

        return {
            "user_id": user_id,
            "new_role": UserRole.ALUMNI.value,
            "status": "graduated",
        }

    def _serialize(self, user: User) -> dict:
        return {
            "id": str(user.id),
            "email": user.email,
            "full_name": user.full_name,
            "display_name": user.display_name,
            "avatar_url": user.avatar_url,
            "phone": user.phone,
            "role": user.role,
            "is_verified": user.is_verified,
            "is_blocked": user.is_blocked,
            "is_active": user.is_active,
            "lgpd_consent_at": user.lgpd_consent_at.isoformat() if user.lgpd_consent_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
        }
