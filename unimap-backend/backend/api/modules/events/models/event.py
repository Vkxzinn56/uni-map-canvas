"""
UniMap 3.0 - Events Domain Models
Public events — accessible to VISITOR+
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity


class Event(BaseEntity):
    __tablename__ = "events"

    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    short_description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, default="general")
    # general | academic | cultural | sports | health | institutional

    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    # Location
    location_name: Mapped[str | None] = mapped_column(String(200), nullable=True)
    block_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("map_blocks.id"), nullable=True
    )
    room_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("map_rooms.id"), nullable=True
    )

    # Media
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_link: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Organizer
    organizer_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )
    organizer_name: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Capacity / Registration
    max_capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    registration_required: Mapped[bool] = mapped_column(default=False, nullable=False)
    registration_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Status
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="published")
    # draft | published | cancelled | completed

    @property
    def is_upcoming(self) -> bool:
        from datetime import timezone
        return self.starts_at > datetime.now(timezone.utc)
