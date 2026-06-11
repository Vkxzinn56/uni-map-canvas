"""
UniMap 3.0 - Events Router
Public: GET (VISITOR+) | Write: PROFESSOR/COORDINATOR/ADMIN
"""
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.events.service.event_service import EventService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import (
    CurrentUser,
    UserRole,
    get_optional_user,
    require_roles,
)

router = APIRouter(prefix="/events", tags=["Events"])


def get_event_service(session: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(session)


@router.get("", summary="List events")
async def list_events(
    category: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    upcoming_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: EventService = Depends(get_event_service),
    current_user: CurrentUser | None = Depends(get_optional_user),
) -> dict:
    """List campus events. Public endpoint — visitor accessible."""
    return await service.list_events(
        category=category,
        date_from=date_from,
        date_to=date_to,
        upcoming_only=upcoming_only,
        skip=skip,
        limit=limit,
    )


@router.get("/{event_id}", summary="Get event details")
async def get_event(
    event_id: uuid.UUID,
    service: EventService = Depends(get_event_service),
) -> dict:
    return await service.get_event(event_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    summary="Create event (PROFESSOR+)",
)
async def create_event(
    body: dict,
    current_user: Annotated[
        CurrentUser,
        Depends(require_roles(UserRole.PROFESSOR, UserRole.COORDINATOR, UserRole.ADMIN)),
    ],
    service: EventService = Depends(get_event_service),
) -> dict:
    return await service.create_event(body, organizer_id=current_user.user_id)


@router.patch("/{event_id}", summary="Update event (PROFESSOR+)")
async def update_event(
    event_id: uuid.UUID,
    body: dict,
    current_user: Annotated[
        CurrentUser,
        Depends(require_roles(UserRole.PROFESSOR, UserRole.COORDINATOR, UserRole.ADMIN)),
    ],
    service: EventService = Depends(get_event_service),
) -> dict:
    return await service.update_event(event_id, body, actor=current_user)


@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel event (COORDINATOR+)",
)
async def cancel_event(
    event_id: uuid.UUID,
    current_user: Annotated[
        CurrentUser,
        Depends(require_roles(UserRole.COORDINATOR, UserRole.ADMIN)),
    ],
    service: EventService = Depends(get_event_service),
) -> None:
    await service.cancel_event(event_id, actor=current_user)
