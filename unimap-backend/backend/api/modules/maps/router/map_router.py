"""
UniMap 3.0 - Maps Router
Public endpoints — accessible to ALL roles (including VISITOR)
GET /api/v1/maps/*
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.maps.schemas.map_schemas import (
    BlockResponse,
    MapOverviewResponse,
    RouteRequest,
    RouteResponse,
)
from backend.api.modules.maps.service.map_service import MapService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import CurrentUser, get_optional_user

router = APIRouter(prefix="/maps", tags=["Campus Map"])


def get_map_service(session: AsyncSession = Depends(get_db)) -> MapService:
    return MapService(session)


@router.get(
    "",
    response_model=MapOverviewResponse,
    summary="Get campus map overview",
    description="Returns all active blocks with coordinates. Publicly accessible.",
)
async def get_map(
    service: MapService = Depends(get_map_service),
    current_user: CurrentUser | None = Depends(get_optional_user),
) -> MapOverviewResponse:
    """
    Full campus map with all blocks and their coordinates.
    No authentication required — visitors can access.
    """
    return await service.get_map_overview()


@router.get(
    "/blocks",
    summary="List all campus blocks",
    description="Returns a list of all blocks/buildings. Public endpoint.",
)
async def get_blocks(
    block_type: str | None = Query(None, description="Filter by block type"),
    service: MapService = Depends(get_map_service),
) -> list[dict]:
    return await service.get_blocks(block_type=block_type)


@router.get(
    "/blocks/{block_code}",
    response_model=BlockResponse,
    summary="Get block details with rooms",
)
async def get_block(
    block_code: str,
    service: MapService = Depends(get_map_service),
) -> BlockResponse:
    return await service.get_block_by_code(block_code)


@router.get(
    "/blocks/{block_code}/rooms",
    summary="Get rooms inside a block",
)
async def get_block_rooms(
    block_code: str,
    floor: int | None = Query(None, description="Filter by floor"),
    room_type: str | None = Query(None, description="Filter by room type"),
    service: MapService = Depends(get_map_service),
) -> list[dict]:
    return await service.get_rooms(block_code=block_code, floor=floor, room_type=room_type)


@router.post(
    "/route",
    response_model=RouteResponse,
    summary="Calculate route between two blocks",
    description="Returns walking directions between campus locations.",
)
async def get_route(
    body: RouteRequest,
    service: MapService = Depends(get_map_service),
) -> RouteResponse:
    """
    Calculate route between two campus blocks.
    Supports accessibility-aware routing.
    """
    return await service.calculate_route(body)
