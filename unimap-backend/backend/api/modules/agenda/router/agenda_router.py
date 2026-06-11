"""
UniMap 3.0 - Agenda Router
Protected: STUDENT / PROFESSOR / COORDINATOR / ADMIN only
VISITOR and unauthenticated users are blocked
"""
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.agenda.service.agenda_service import AgendaService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import (
    AcademicOnly,
    CurrentUser,
    UserRole,
    get_current_user,
    require_roles,
)

router = APIRouter(prefix="/agenda", tags=["Agenda"])


def get_agenda_service(session: AsyncSession = Depends(get_db)) -> AgendaService:
    return AgendaService(session)


@router.get(
    "",
    dependencies=[AcademicOnly],
    summary="Get student agenda",
    description="Returns the authenticated student's class schedule. STUDENT+ only.",
)
async def get_agenda(
    week_start: date | None = Query(None, description="ISO date of the week's Monday"),
    semester: str | None = Query(None, description="e.g. 2024-1"),
    current_user: CurrentUser = Depends(get_current_user),
    service: AgendaService = Depends(get_agenda_service),
) -> dict:
    return await service.get_agenda(
        user_id=current_user.user_id,
        week_start=week_start,
        semester=semester,
    )


@router.get(
    "/classes",
    dependencies=[AcademicOnly],
    summary="List classes in schedule",
)
async def get_classes(
    subject_code: str | None = Query(None),
    day_of_week: int | None = Query(None, ge=0, le=6),
    current_user: CurrentUser = Depends(get_current_user),
    service: AgendaService = Depends(get_agenda_service),
) -> list[dict]:
    return await service.get_classes(
        user_id=current_user.user_id,
        subject_code=subject_code,
        day_of_week=day_of_week,
    )


@router.get(
    "/activities",
    dependencies=[AcademicOnly],
    summary="List academic activities and deadlines",
)
async def get_activities(
    activity_type: str | None = Query(None),
    pending_only: bool = Query(False),
    current_user: CurrentUser = Depends(get_current_user),
    service: AgendaService = Depends(get_agenda_service),
) -> list[dict]:
    return await service.get_activities(
        user_id=current_user.user_id,
        activity_type=activity_type,
        pending_only=pending_only,
    )


@router.post(
    "/activities",
    dependencies=[AcademicOnly],
    summary="Create personal activity/reminder",
    status_code=201,
)
async def create_activity(
    body: dict,
    current_user: CurrentUser = Depends(get_current_user),
    service: AgendaService = Depends(get_agenda_service),
) -> dict:
    return await service.create_activity(user_id=current_user.user_id, data=body)


@router.patch(
    "/activities/{activity_id}",
    dependencies=[AcademicOnly],
    summary="Update activity (mark complete, edit)",
)
async def update_activity(
    activity_id: uuid.UUID,
    body: dict,
    current_user: CurrentUser = Depends(get_current_user),
    service: AgendaService = Depends(get_agenda_service),
) -> dict:
    return await service.update_activity(
        activity_id=activity_id,
        user_id=current_user.user_id,
        data=body,
    )
