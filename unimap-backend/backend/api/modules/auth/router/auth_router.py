"""
UniMap 3.0 - Auth Router
REST API: /api/v1/auth/*
Rate limited with SlowAPI
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.auth.schemas.auth_schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    LoginResponse,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from backend.api.modules.auth.service.auth_service import AuthService
from backend.shared.cache.redis_service import CacheService, get_cache
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import CurrentUser, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
limiter = Limiter(key_func=get_remote_address)


def get_auth_service(
    session: AsyncSession = Depends(get_db),
    cache: CacheService = Depends(get_cache),
) -> AuthService:
    return AuthService(session, cache)


@router.post(
    "/register",
    response_model=LoginResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
)
@limiter.limit("5/minute")
async def register(
    request: Request,
    body: RegisterRequest,
    service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """
    Register a new user account.
    - LGPD consent is required
    - Default role: VISITOR
    """
    ip = request.client.host if request.client else None
    return await service.register(body, ip_address=ip)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Login and obtain tokens",
)
@limiter.limit("10/minute")
async def login(
    request: Request,
    body: LoginRequest,
    service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    """
    Authenticate and receive access + refresh token pair.
    - Brute-force protection: locked after 5 failed attempts
    """
    ip = request.client.host if request.client else None
    ua = request.headers.get("User-Agent")
    return await service.login(body, ip_address=ip, user_agent=ua)


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token",
)
@limiter.limit("30/minute")
async def refresh(
    request: Request,
    body: RefreshRequest,
    service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Exchange a valid refresh token for a new token pair."""
    return await service.refresh_tokens(body.refresh_token)


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Revoke current token",
)
async def logout(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    service: AuthService = Depends(get_auth_service),
) -> None:
    """Revoke the current access token (adds to blacklist)."""
    await service.logout(current_user.jti)


@router.post(
    "/forgot-password",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Request password reset email",
)
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    body: ForgotPasswordRequest,
    service: AuthService = Depends(get_auth_service),
) -> dict:
    """
    Send password reset email.
    Always returns 202 to prevent user enumeration.
    """
    # TODO: Implement email dispatch via notification service
    return {"message": "If the email exists, a reset link has been sent"}


@router.get(
    "/me",
    summary="Get current authenticated user",
)
async def get_me(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Returns identity claims from the current token."""
    return {
        "user_id": current_user.user_id,
        "role": current_user.role.value,
    }
