"""
UniMap 3.0 - Audit Router Service
Application Layer: Audit log queries for compliance
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.audit.models.audit_log import AuditAction, AuditLog
from backend.api.modules.users.repository.user_repository import UserRepository
from backend.shared.exceptions.auth import NotFoundException


class AuditRouterService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._user_repo = UserRepository(session)

    async def list_logs(
        self,
        actor_id: str | None = None,
        resource_type: str | None = None,
        action: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> dict:
        stmt = select(AuditLog)
        if actor_id:
            stmt = stmt.where(AuditLog.actor_id == actor_id)
        if resource_type:
            stmt = stmt.where(AuditLog.resource_type == resource_type)
        if action:
            stmt = stmt.where(AuditLog.action == action)
        if date_from:
            stmt = stmt.where(
                AuditLog.timestamp >= datetime.combine(date_from, datetime.min.time())
            )
        if date_to:
            stmt = stmt.where(
                AuditLog.timestamp <= datetime.combine(date_to, datetime.max.time())
            )

        total_stmt = stmt.with_only_columns(AuditLog.id)
        total_result = await self._session.execute(total_stmt)
        total = len(total_result.all())

        stmt = stmt.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        logs = result.scalars().all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [self._serialize(log) for log in logs],
        }

    async def get_log(self, log_id: uuid.UUID) -> dict:
        stmt = select(AuditLog).where(AuditLog.id == log_id)
        result = await self._session.execute(stmt)
        log = result.scalar_one_or_none()
        if not log:
            raise NotFoundException("AuditLog", str(log_id))
        return self._serialize(log, detail=True)

    async def user_history(self, user_id: uuid.UUID) -> list[dict]:
        stmt = (
            select(AuditLog)
            .where(AuditLog.actor_id == str(user_id))
            .order_by(AuditLog.timestamp.desc())
            .limit(500)
        )
        result = await self._session.execute(stmt)
        logs = result.scalars().all()
        return [self._serialize(log) for log in logs]

    async def anonymize_user(self, user_id: uuid.UUID, actor_id: str) -> dict:
        """LGPD: anonymize and log the action."""
        success = await self._user_repo.anonymize(user_id)
        if not success:
            raise NotFoundException("User", str(user_id))

        # Log the anonymization
        entry = AuditLog(
            actor_id=actor_id,
            action=AuditAction.ANONYMIZE.value,
            resource_type="User",
            resource_id=str(user_id),
            metadata={"lgpd": True, "reason": "user_request_or_admin_action"},
        )
        self._session.add(entry)
        await self._session.flush()

        return {
            "success": True,
            "user_id": str(user_id),
            "anonymized_at": datetime.now(timezone.utc).isoformat(),
        }

    def _serialize(self, log: AuditLog, detail: bool = False) -> dict:
        base = {
            "id": str(log.id),
            "timestamp": log.timestamp.isoformat(),
            "actor_id": log.actor_id,
            "actor_role": log.actor_role,
            "action": log.action,
            "resource_type": log.resource_type,
            "resource_id": log.resource_id,
            "success": log.success,
        }
        if detail:
            base["ip_address"] = log.ip_address
            base["user_agent"] = log.user_agent
            base["metadata"] = log.metadata
            base["request_id"] = log.request_id
        return base
