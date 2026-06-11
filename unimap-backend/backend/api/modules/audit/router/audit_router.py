"""
UniMap 3.0 - Audit Router
Admin/Coordinator only — compliance and LGPD audit trail
"""
import uuid
from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.audit.service.audit_router_service import AuditRouterService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import (
    AdminOnly,
    CurrentUser,
    StaffOnly,
    UserRole,
    get_current_user,
    require_roles,
)

router = APIRouter(prefix="/audit", tags=["Audit"])


def get_audit_service(session: AsyncSession = Depends(get_db)) -> AuditRouterService:
    return AuditRouterService(session)


@router.get(
    "/logs",
    dependencies=[StaffOnly],
    summary="List audit logs (COORDINATOR+)",
)
async def list_audit_logs(
    actor_id: str | None = Query(None),
    resource_type: str | None = Query(None),
    action: str | None = Query(None),
    date_from: date | None = Query(None),
    date_to: date | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: AuditRouterService = Depends(get_audit_service),
) -> dict:
    return await service.list_logs(
        actor_id=actor_id,
        resource_type=resource_type,
        action=action,
        date_from=date_from,
        date_to=date_to,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/logs/{log_id}",
    dependencies=[StaffOnly],
    summary="Get audit log detail",
)
async def get_audit_log(
    log_id: uuid.UUID,
    service: AuditRouterService = Depends(get_audit_service),
) -> dict:
    return await service.get_log(log_id)


@router.get(
    "/users/{user_id}/history",
    dependencies=[AdminOnly],
    summary="Full activity history for a user (ADMIN only)",
)
async def user_history(
    user_id: uuid.UUID,
    service: AuditRouterService = Depends(get_audit_service),
) -> list[dict]:
    return await service.user_history(user_id)


@router.post(
    "/lgpd/anonymize/{user_id}",
    dependencies=[AdminOnly],
    summary="LGPD anonymize user data (ADMIN only)",
)
async def anonymize_user(
    user_id: uuid.UUID,
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: AuditRouterService = Depends(get_audit_service),
) -> dict:
    return await service.anonymize_user(user_id, actor_id=current_user.user_id)
