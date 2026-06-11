"""
UniMap 3.0 - Auth Service
Application Layer: Authentication and token management
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.users.models.user import User
from backend.api.modules.users.repository.user_repository import UserRepository
from backend.api.modules.audit.models.audit_log import AuditAction, AuditService
from backend.api.modules.auth.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    TokenResponse,
    AuthUserResponse,
)
from backend.core.config.settings import settings
from backend.shared.exceptions.auth import (
    AccountBlockedException,
    AlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
)
from backend.shared.security.jwt import password_service, token_service
from backend.shared.security.rbac import UserRole
from backend.shared.cache.redis_service import CacheService


MAX_FAILED_ATTEMPTS = 5
LOCKOUT_MINUTES = 15


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        cache: CacheService,
    ) -> None:
        self._session = session
        self._user_repo = UserRepository(session)
        self._audit = AuditService(session)
        self._cache = cache

    async def register(
        self,
        data: RegisterRequest,
        ip_address: str | None = None,
    ) -> LoginResponse:
        # Check duplicate
        existing = await self._user_repo.find_by_email(data.email)
        if existing:
            raise AlreadyExistsException("User", "email")

        # Create user
        user = User(
            email=data.email,
            hashed_password=password_service.hash(data.password),
            full_name=data.full_name,
            role=UserRole.VISITOR.value,
            lgpd_consent_at=datetime.now(timezone.utc),
            lgpd_consent_ip=ip_address,
        )
        user = await self._user_repo.save(user)

        await self._audit.log(
            AuditAction.CREATE,
            "User",
            str(user.id),
            actor_id=str(user.id),
            ip_address=ip_address,
            metadata={"email": user.email, "role": user.role},
        )

        return await self._build_login_response(user)

    async def login(
        self,
        data: LoginRequest,
        ip_address: str | None = None,
        user_agent: str | None = None,
    ) -> LoginResponse:
        user = await self._user_repo.find_by_email(data.email)

        if not user:
            raise InvalidCredentialsException()

        # Check lockout
        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise AccountBlockedException("Account temporarily locked. Try again later.")

        if user.is_blocked:
            raise AccountBlockedException(user.block_reason or "Account blocked")

        # Verify password
        if not password_service.verify(data.password, user.hashed_password):
            await self._handle_failed_login(user)
            raise InvalidCredentialsException()

        # Reset failed attempts on success
        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.now(timezone.utc)
        user.last_login_ip = ip_address
        await self._user_repo.save(user)

        await self._audit.log(
            AuditAction.LOGIN,
            "User",
            str(user.id),
            actor_id=str(user.id),
            actor_role=user.role,
            ip_address=ip_address,
            user_agent=user_agent,
        )

        return await self._build_login_response(user)

    async def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        payload = token_service.decode_refresh(refresh_token)

        # Check if token is revoked
        jti = payload.get("jti", "")
        if await self._cache.exists(f"revoked_token:{jti}"):
            raise InvalidTokenException("Token has been revoked")

        user = await self._user_repo.find_by_id(uuid.UUID(payload["sub"]))
        if not user or user.is_blocked:
            raise InvalidTokenException()

        access, new_refresh = token_service.create_token_pair(
            str(user.id), user.role
        )

        # Revoke old refresh token
        ttl = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS * 86400
        await self._cache.set(f"revoked_token:{jti}", "1", ttl)

        return TokenResponse(
            access_token=access,
            refresh_token=new_refresh,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    async def logout(self, jti: str) -> None:
        ttl = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        await self._cache.set(f"revoked_token:{jti}", "1", ttl)

    async def _handle_failed_login(self, user: User) -> None:
        from datetime import timedelta

        user.failed_login_attempts += 1
        if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
            user.locked_until = datetime.now(timezone.utc) + timedelta(
                minutes=LOCKOUT_MINUTES
            )
        await self._user_repo.save(user)

    async def _build_login_response(self, user: User) -> LoginResponse:
        access, refresh = token_service.create_token_pair(str(user.id), user.role)
        return LoginResponse(
            tokens=TokenResponse(
                access_token=access,
                refresh_token=refresh,
                token_type="bearer",
                expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            ),
            user=AuthUserResponse(
                id=str(user.id),
                email=user.email,
                full_name=user.full_name,
                role=user.role,
                is_verified=user.is_verified,
                created_at=user.created_at,
            ),
        )
