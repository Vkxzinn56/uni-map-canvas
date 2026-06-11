"""
UniMap 3.0 - Events Service
Application Layer: Event management
"""
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.events.models.event import Event
from backend.shared.exceptions.auth import NotFoundException, BusinessRuleException
from backend.shared.security.rbac import CurrentUser, UserRole


class EventService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_events(
        self,
        category: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        upcoming_only: bool = True,
        skip: int = 0,
        limit: int = 20,
    ) -> dict:
        stmt = select(Event).where(
            Event.deleted_at.is_(None),
            Event.status == "published",
        )
        if upcoming_only:
            stmt = stmt.where(Event.starts_at > datetime.now(timezone.utc))
        if category:
            stmt = stmt.where(Event.category == category)
        if date_from:
            stmt = stmt.where(Event.starts_at >= datetime.combine(date_from, datetime.min.time()))
        if date_to:
            stmt = stmt.where(Event.ends_at <= datetime.combine(date_to, datetime.max.time()))

        count_result = await self._session.execute(
            stmt.with_only_columns(Event.id)
        )
        total = len(count_result.all())

        stmt = stmt.order_by(Event.starts_at).offset(skip).limit(limit)
        result = await self._session.execute(stmt)
        events = result.scalars().all()

        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "items": [self._serialize(e) for e in events],
        }

    async def get_event(self, event_id: uuid.UUID) -> dict:
        stmt = select(Event).where(
            Event.id == event_id, Event.deleted_at.is_(None)
        )
        result = await self._session.execute(stmt)
        event = result.scalar_one_or_none()
        if not event:
            raise NotFoundException("Event", str(event_id))
        return self._serialize(event, detail=True)

    async def create_event(self, data: dict, organizer_id: str) -> dict:
        event = Event(
            title=data["title"],
            description=data.get("description"),
            short_description=data.get("short_description"),
            category=data.get("category", "general"),
            starts_at=datetime.fromisoformat(data["starts_at"]),
            ends_at=datetime.fromisoformat(data["ends_at"]),
            location_name=data.get("location_name"),
            organizer_id=uuid.UUID(organizer_id),
            organizer_name=data.get("organizer_name"),
            max_capacity=data.get("max_capacity"),
            registration_required=data.get("registration_required", False),
            status="published",
        )
        self._session.add(event)
        await self._session.flush()
        return self._serialize(event)

    async def update_event(
        self, event_id: uuid.UUID, data: dict, actor: CurrentUser
    ) -> dict:
        event = await self._get_or_404(event_id)
        # Only organizer or COORDINATOR+ can edit
        if (
            str(event.organizer_id) != actor.user_id
            and actor.role not in (UserRole.COORDINATOR, UserRole.ADMIN)
        ):
            raise BusinessRuleException("Only the organizer or coordinator can edit this event")

        for field in ("title", "description", "category", "status", "location_name"):
            if field in data:
                setattr(event, field, data[field])
        await self._session.flush()
        return self._serialize(event)

    async def cancel_event(self, event_id: uuid.UUID, actor: CurrentUser) -> None:
        event = await self._get_or_404(event_id)
        event.status = "cancelled"
        await self._session.flush()

    async def _get_or_404(self, event_id: uuid.UUID) -> Event:
        stmt = select(Event).where(Event.id == event_id, Event.deleted_at.is_(None))
        result = await self._session.execute(stmt)
        event = result.scalar_one_or_none()
        if not event:
            raise NotFoundException("Event", str(event_id))
        return event

    def _serialize(self, event: Event, detail: bool = False) -> dict:
        base = {
            "id": str(event.id),
            "title": event.title,
            "short_description": event.short_description,
            "category": event.category,
            "starts_at": event.starts_at.isoformat(),
            "ends_at": event.ends_at.isoformat(),
            "location_name": event.location_name,
            "image_url": event.image_url,
            "status": event.status,
            "registration_required": event.registration_required,
            "registration_url": event.registration_url,
        }
        if detail:
            base["description"] = event.description
            base["organizer_name"] = event.organizer_name
            base["max_capacity"] = event.max_capacity
            base["external_link"] = event.external_link
        return base
