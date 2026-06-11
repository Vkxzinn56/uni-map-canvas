"""
UniMap 3.0 - Maps Schemas
"""
from uuid import UUID

from pydantic import BaseModel, Field


class CoordinatesSchema(BaseModel):
    latitude: float
    longitude: float


class RoomResponse(BaseModel):
    id: UUID
    code: str
    name: str
    floor: int
    capacity: int | None
    room_type: str
    is_active: bool

    model_config = {"from_attributes": True}


class BlockResponse(BaseModel):
    id: UUID
    code: str
    name: str
    short_name: str | None
    block_type: str
    description: str | None
    floor_count: int
    latitude: float | None
    longitude: float | None
    geojson: dict | None
    image_url: str | None
    is_active: bool
    rooms: list[RoomResponse] = []

    model_config = {"from_attributes": True}


class BlockListResponse(BaseModel):
    id: UUID
    code: str
    name: str
    short_name: str | None
    block_type: str
    latitude: float | None
    longitude: float | None

    model_config = {"from_attributes": True}


class MapOverviewResponse(BaseModel):
    campus_name: str
    total_blocks: int
    total_rooms: int
    blocks: list[BlockListResponse]
    center: CoordinatesSchema | None


class RouteRequest(BaseModel):
    origin_block_code: str
    destination_block_code: str
    accessibility: bool = False


class WaypointSchema(BaseModel):
    latitude: float
    longitude: float
    label: str | None = None


class RouteResponse(BaseModel):
    id: UUID | None
    origin_label: str
    destination_label: str
    distance_meters: float | None
    duration_minutes: float | None
    is_accessible: bool
    waypoints: list[WaypointSchema]

    model_config = {"from_attributes": True}
