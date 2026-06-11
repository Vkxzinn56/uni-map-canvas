"""
UniMap 3.0 - Notifications Service
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.notifications.models.notification import Notification
from backend.shared.exceptions.auth import NotFoundException


class NotificationService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(
        self,
        recipient_id: str,
        title: str,
        body: str,
        notification_type: str,
        reference_type: str | None = None,
        reference_id: str | None = None,
        sender_id: str | None = None,
        channels: list[str] | None = None,
        metadata: dict | None = None,
    ) -> Notification:
        notif = Notification(
            recipient_id=uuid.UUID(recipient_id),
            title=title,
            body=body,
            notification_type=notification_type,
            reference_type=reference_type,
            reference_id=reference_id,
            sender_id=uuid.UUID(sender_id) if sender_id else None,
            channels=channels or ["in_app"],
            metadata=metadata,
        )
        self._session.add(notif)
        await self._session.flush()
        return notif

    async def get_notifications(
        self,
        user_id: str,
        unread_only: bool = False,
        notification_type: str | None = None,
        skip: int = 0,
        limit: int = 20,
    ) -> dict:
        stmt = select(Notification).where(
            Notification.recipient_id == uuid.UUID(user_id),
            Notification.deleted_at.is_(None),
        )
        if unread_only:
            stmt = stmt.where(Notification.is_read == False)
        if notification_type:
            stmt = stmt.where(Notification.notification_type == notification_type)

        total_stmt = stmt.with_only_columns(func.count())
        total_result = await self._session.execute(total_stmt)
        total = total_result.scalar_one()

        stmt = stmt.order_by(Notification.created_at.desc()).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        notifs = result.scalars().all()

        return {
            "total": total,
            "items": [
                {
                    "id": str(n.id),
                    "title": n.title,
                    "body": n.body,
                    "notification_type": n.notification_type,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat(),
                    "reference_type": n.reference_type,
                    "reference_id": n.reference_id,
                }
                for n in notifs
            ],
        }

    async def mark_read(self, notification_id: uuid.UUID, user_id: str) -> None:
        stmt = select(Notification).where(
            Notification.id == notification_id,
            Notification.recipient_id == uuid.UUID(user_id),
        )
        result = await self._session.execute(stmt)
        notif = result.scalar_one_or_none()
        if not notif:
            raise NotFoundException("Notification", str(notification_id))
        notif.is_read = True
        notif.read_at = datetime.now(timezone.utc)
        await self._session.flush()

    async def mark_all_read(self, user_id: str) -> int:
        stmt = (
            update(Notification)
            .where(
                Notification.recipient_id == uuid.UUID(user_id),
                Notification.is_read == False,
                Notification.deleted_at.is_(None),
            )
            .values(is_read=True, read_at=datetime.now(timezone.utc))
        )
        result = await self._session.execute(stmt)
        return result.rowcount

    async def count_unread(self, user_id: str) -> int:
        stmt = select(func.count()).where(
            Notification.recipient_id == uuid.UUID(user_id),
            Notification.is_read == False,
            Notification.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        return result.scalar_one()
