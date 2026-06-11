"""
UniMap 3.0 - RBAC (Role-Based Access Control)
Security: Roles, Permissions, and FastAPI Dependencies
"""
from enum import StrEnum
from functools import wraps
from typing import Annotated

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.shared.exceptions.auth import (
    InsufficientPermissionsException,
    InvalidTokenException,
)
from backend.shared.security.jwt import token_service

security = HTTPBearer(auto_error=False)


# ─── Roles ────────────────────────────────────────────────────────────────────
class UserRole(StrEnum):
    VISITOR = "visitor"
    STUDENT = "student"
    PROFESSOR = "professor"
    COORDINATOR = "coordinator"
    ADMIN = "admin"
    ALUMNI = "alumni"  # Graduated — read-only history


# ─── Permission Sets ──────────────────────────────────────────────────────────
ROLE_PERMISSIONS: dict[UserRole, set[str]] = {
    UserRole.VISITOR: {
        "map:read",
        "clinics:read",
        "events:read",
        "services:read",
    },
    UserRole.ALUMNI: {
        "map:read",
        "clinics:read",
        "events:read",
        "services:read",
        "history:read",  # Own academic history only
    },
    UserRole.STUDENT: {
        "map:read",
        "clinics:read",
        "clinics:write",
        "events:read",
        "services:read",
        "agenda:read",
        "classes:read",
        "academic:read",
        "notifications:read",
        "profile:read",
        "profile:write",
    },
    UserRole.PROFESSOR: {
        "map:read",
        "map:write",
        "clinics:read",
        "events:read",
        "events:write",
        "agenda:read",
        "agenda:write",
        "classes:read",
        "classes:write",
        "academic:read",
        "notifications:read",
        "notifications:write",
        "profile:read",
        "profile:write",
        "blackboard:read",
    },
    UserRole.COORDINATOR: {
        "*:read",
        "events:write",
        "agenda:write",
        "clinics:write",
        "map:write",
        "blackboard:read",
        "blackboard:write",
        "reports:read",
        "notifications:write",
        "profile:read",
        "profile:write",
    },
    UserRole.ADMIN: {
        "*",  # Full access
    },
}


def has_permission(role: UserRole, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    if "*" in perms:
        return True
    resource = permission.split(":")[0]
    if f"{resource}:*" in perms or f"*:*" in perms:
        return True
    # Check wildcard read/write per resource
    for perm in perms:
        if perm.endswith(":*") and perm.startswith(resource):
            return True
    return permission in perms


# ─── Current User ─────────────────────────────────────────────────────────────
class CurrentUser:
    def __init__(self, user_id: str, role: UserRole, jti: str) -> None:
        self.user_id = user_id
        self.role = role
        self.jti = jti

    def can(self, permission: str) -> bool:
        return has_permission(self.role, permission)

    def require(self, permission: str) -> None:
        if not self.can(permission):
            raise InsufficientPermissionsException(permission)


# ─── FastAPI Dependencies ─────────────────────────────────────────────────────
async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
) -> CurrentUser:
    if not credentials:
        raise InvalidTokenException("No token provided")
    payload = token_service.decode_access(credentials.credentials)
    return CurrentUser(
        user_id=payload["sub"],
        role=UserRole(payload["role"]),
        jti=payload.get("jti", ""),
    )


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
) -> CurrentUser | None:
    if not credentials:
        return None
    try:
        payload = token_service.decode_access(credentials.credentials)
        return CurrentUser(
            user_id=payload["sub"],
            role=UserRole(payload["role"]),
            jti=payload.get("jti", ""),
        )
    except Exception:
        return None


def require_roles(*roles: UserRole):
    """Dependency factory for role-gated endpoints."""

    async def checker(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        if current_user.role not in roles:
            raise InsufficientPermissionsException(
                f"Requires one of: {[r.value for r in roles]}"
            )
        return current_user

    return checker


def require_permission(permission: str):
    """Dependency factory for permission-gated endpoints."""

    async def checker(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        current_user.require(permission)
        return current_user

    return checker


# ─── Convenient typed dependencies ────────────────────────────────────────────
AdminOnly = Depends(require_roles(UserRole.ADMIN))
StaffOnly = Depends(require_roles(UserRole.ADMIN, UserRole.COORDINATOR))
AcademicOnly = Depends(
    require_roles(
        UserRole.STUDENT, UserRole.PROFESSOR, UserRole.COORDINATOR, UserRole.ADMIN
    )
)
