"""
UniMap 3.0 - Campus Map Domain Models
Public resource — accessible to all roles including VISITOR
"""
import uuid
from enum import StrEnum

from sqlalchemy import Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity


class BlockType(StrEnum):
    ACADEMIC = "academic"
    ADMINISTRATIVE = "administrative"
    SPORTS = "sports"
    LIBRARY = "library"
    FOOD = "food"
    CLINIC = "clinic"
    PARKING = "parking"
    OTHER = "other"


class Block(BaseEntity):
    """Campus building/block."""

    __tablename__ = "map_blocks"

    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    short_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    block_type: Mapped[str] = mapped_column(String(50), nullable=False, default=BlockType.ACADEMIC)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    floor_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Geolocation
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)

    # GeoJSON polygon for the block footprint
    geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    rooms: Mapped[list["Room"]] = relationship(
        "Room", back_populates="block", lazy="select"
    )

    @property
    def coordinates(self) -> tuple[float, float] | None:
        if self.latitude and self.longitude:
            return (self.latitude, self.longitude)
        return None


class Room(BaseEntity):
    """Room/space inside a block."""

    __tablename__ = "map_rooms"

    block_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("map_blocks.id"), nullable=False, index=True
    )
    code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    floor: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    capacity: Mapped[int | None] = mapped_column(Integer, nullable=True)
    room_type: Mapped[str] = mapped_column(String(50), nullable=False, default="classroom")
    # classroom | lab | office | auditorium | bathroom | stairwell | elevator
    amenities: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    # Relationships
    block: Mapped["Block"] = relationship("Block", back_populates="rooms")


class MapRoute(BaseEntity):
    """Pre-computed accessible route between two points."""

    __tablename__ = "map_routes"

    origin_block_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("map_blocks.id"), nullable=True
    )
    destination_block_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("map_blocks.id"), nullable=True
    )
    origin_label: Mapped[str] = mapped_column(String(200), nullable=False)
    destination_label: Mapped[str] = mapped_column(String(200), nullable=False)
    distance_meters: Mapped[float | None] = mapped_column(Float, nullable=True)
    duration_minutes: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_accessible: Mapped[bool] = mapped_column(default=True, nullable=False)
    waypoints: Mapped[list | None] = mapped_column(JSON, nullable=True)
    # [{lat, lng, label}, ...]
