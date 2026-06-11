"""
UniMap 3.0 - Notifications Router
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.notifications.service.notification_service import NotificationService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import CurrentUser, get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


def get_notification_service(session: AsyncSession = Depends(get_db)) -> NotificationService:
    return NotificationService(session)


@router.get("", summary="Get my notifications")
async def get_notifications(
    unread_only: bool = Query(False),
    notification_type: str | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=50),
    current_user: CurrentUser = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    return await service.get_notifications(
        user_id=current_user.user_id,
        unread_only=unread_only,
        notification_type=notification_type,
        skip=skip,
        limit=limit,
    )


@router.post("/{notification_id}/read", summary="Mark notification as read")
async def mark_read(
    notification_id: uuid.UUID,
    current_user: CurrentUser = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    await service.mark_read(notification_id, user_id=current_user.user_id)
    return {"success": True}


@router.post("/read-all", summary="Mark all notifications as read")
async def mark_all_read(
    current_user: CurrentUser = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    count = await service.mark_all_read(user_id=current_user.user_id)
    return {"marked_count": count}


@router.get("/unread-count", summary="Get unread notification count")
async def unread_count(
    current_user: CurrentUser = Depends(get_current_user),
    service: NotificationService = Depends(get_notification_service),
) -> dict:
    count = await service.count_unread(user_id=current_user.user_id)
    return {"count": count}
