"""
UniMap 3.0 - Map Service
Application Layer: Campus map business logic
"""
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.api.modules.maps.models.map_models import Block, MapRoute, Room
from backend.api.modules.maps.schemas.map_schemas import (
    BlockListResponse,
    BlockResponse,
    CoordinatesSchema,
    MapOverviewResponse,
    RouteRequest,
    RouteResponse,
    WaypointSchema,
)
from backend.shared.exceptions.auth import NotFoundException


class MapService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_map_overview(self) -> MapOverviewResponse:
        stmt = (
            select(Block)
            .where(Block.deleted_at.is_(None), Block.is_active == True)
            .order_by(Block.code)
        )
        result = await self._session.execute(stmt)
        blocks = list(result.scalars().all())

        # Count rooms
        room_stmt = select(Room).where(
            Room.deleted_at.is_(None), Room.is_active == True
        )
        room_result = await self._session.execute(room_stmt)
        total_rooms = len(list(room_result.scalars().all()))

        # Compute center (centroid of all geolocated blocks)
        geolocated = [b for b in blocks if b.latitude and b.longitude]
        center = None
        if geolocated:
            center = CoordinatesSchema(
                latitude=sum(b.latitude for b in geolocated) / len(geolocated),
                longitude=sum(b.longitude for b in geolocated) / len(geolocated),
            )

        return MapOverviewResponse(
            campus_name="Campus UniMap",
            total_blocks=len(blocks),
            total_rooms=total_rooms,
            blocks=[BlockListResponse.model_validate(b) for b in blocks],
            center=center,
        )

    async def get_blocks(self, block_type: str | None = None) -> list[dict]:
        stmt = select(Block).where(
            Block.deleted_at.is_(None), Block.is_active == True
        )
        if block_type:
            stmt = stmt.where(Block.block_type == block_type)
        stmt = stmt.order_by(Block.code)
        result = await self._session.execute(stmt)
        blocks = result.scalars().all()
        return [BlockListResponse.model_validate(b).model_dump() for b in blocks]

    async def get_block_by_code(self, code: str) -> BlockResponse:
        stmt = (
            select(Block)
            .options(selectinload(Block.rooms))
            .where(Block.code == code.upper(), Block.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        block = result.scalar_one_or_none()
        if not block:
            raise NotFoundException("Block", code)
        return BlockResponse.model_validate(block)

    async def get_rooms(
        self,
        block_code: str,
        floor: int | None = None,
        room_type: str | None = None,
    ) -> list[dict]:
        block = await self.get_block_by_code(block_code)
        stmt = select(Room).join(Block).where(
            Block.code == block_code.upper(),
            Room.deleted_at.is_(None),
            Room.is_active == True,
        )
        if floor is not None:
            stmt = stmt.where(Room.floor == floor)
        if room_type:
            stmt = stmt.where(Room.room_type == room_type)
        result = await self._session.execute(stmt)
        rooms = result.scalars().all()
        return [
            {
                "id": str(r.id),
                "code": r.code,
                "name": r.name,
                "floor": r.floor,
                "capacity": r.capacity,
                "room_type": r.room_type,
            }
            for r in rooms
        ]

    async def calculate_route(self, request: RouteRequest) -> RouteResponse:
        """
        Find pre-computed route or generate basic route.
        Future: integrate with campus GIS/pathfinding engine.
        """
        # Try stored route first
        stmt = (
            select(MapRoute)
            .join(Block, MapRoute.origin_block_id == Block.id)
            .where(Block.code == request.origin_block_code.upper())
        )
        result = await self._session.execute(stmt)
        route = result.scalar_one_or_none()

        if route:
            waypoints = [
                WaypointSchema(**wp) for wp in (route.waypoints or [])
            ]
            return RouteResponse(
                id=route.id,
                origin_label=route.origin_label,
                destination_label=route.destination_label,
                distance_meters=route.distance_meters,
                duration_minutes=route.duration_minutes,
                is_accessible=route.is_accessible,
                waypoints=waypoints,
            )

        # Fallback: direct point-to-point
        origin = await self._get_block_coords(request.origin_block_code)
        dest = await self._get_block_coords(request.destination_block_code)

        return RouteResponse(
            id=None,
            origin_label=request.origin_block_code,
            destination_label=request.destination_block_code,
            distance_meters=None,
            duration_minutes=None,
            is_accessible=request.accessibility,
            waypoints=[origin, dest] if (origin and dest) else [],
        )

    async def _get_block_coords(self, code: str) -> WaypointSchema | None:
        stmt = select(Block).where(Block.code == code.upper())
        result = await self._session.execute(stmt)
        block = result.scalar_one_or_none()
        if block and block.latitude and block.longitude:
            return WaypointSchema(
                latitude=block.latitude,
                longitude=block.longitude,
                label=block.name,
            )
        return None
