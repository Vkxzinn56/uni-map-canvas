"""
UniMap 3.0 - Users Router
Profile management, admin user CRUD
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.users.service.user_service import UserService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import (
    AdminOnly,
    CurrentUser,
    UserRole,
    get_current_user,
    require_roles,
)

router = APIRouter(prefix="/users", tags=["Users"])


def get_user_service(session: AsyncSession = Depends(get_db)) -> UserService:
    return UserService(session)


# ─── Self (any authenticated user) ───────────────────────────────────────────

@router.get("/me", summary="Get my profile")
async def get_my_profile(
    current_user: CurrentUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.get_profile(current_user.user_id)


@router.patch("/me", summary="Update my profile")
async def update_my_profile(
    body: dict,
    current_user: CurrentUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.update_profile(current_user.user_id, body)


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete my account (LGPD right to erasure)",
)
async def delete_my_account(
    current_user: CurrentUser = Depends(get_current_user),
    service: UserService = Depends(get_user_service),
) -> None:
    await service.request_deletion(current_user.user_id)


# ─── Admin (ADMIN only) ────────────────────────────────────────────────────────

@router.get(
    "",
    dependencies=[AdminOnly],
    summary="List all users (ADMIN)",
)
async def list_users(
    role: str | None = Query(None),
    is_active: bool | None = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.list_users(role=role, is_active=is_active, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    dependencies=[AdminOnly],
    summary="Get user by ID (ADMIN)",
)
async def get_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.get_profile(str(user_id))


@router.patch(
    "/{user_id}/role",
    dependencies=[AdminOnly],
    summary="Change user role (ADMIN)",
)
async def change_role(
    user_id: uuid.UUID,
    body: dict,
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.change_role(str(user_id), body["role"])


@router.post(
    "/{user_id}/block",
    dependencies=[AdminOnly],
    summary="Block user (ADMIN)",
)
async def block_user(
    user_id: uuid.UUID,
    body: dict,
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.block_user(str(user_id), body.get("reason", "Admin action"))


@router.post(
    "/{user_id}/unblock",
    dependencies=[AdminOnly],
    summary="Unblock user (ADMIN)",
)
async def unblock_user(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> dict:
    return await service.unblock_user(str(user_id))


@router.post(
    "/{user_id}/graduate",
    dependencies=[AdminOnly],
    summary="Graduate student → ALUMNI (ADMIN)",
)
async def graduate_student(
    user_id: uuid.UUID,
    service: UserService = Depends(get_user_service),
) -> dict:
    """
    Marks student as graduated.
    - Role changed to ALUMNI
    - Access to academic data blocked
    - History preserved (LGPD)
    """
    return await service.graduate_student(str(user_id))
