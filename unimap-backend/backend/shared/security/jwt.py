"""
UniMap 3.0 - JWT Service
Security: Access + Refresh token pair with RBAC claims
"""
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from backend.core.config.settings import settings
from backend.shared.exceptions.auth import (
    InvalidTokenException,
    TokenExpiredException,
)

# ─── Password Hashing (Argon2) ────────────────────────────────────────────────
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__time_cost=2,
    argon2__memory_cost=65536,
    argon2__parallelism=2,
)


class PasswordService:
    @staticmethod
    def hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain: str, hashed: str) -> bool:
        return pwd_context.verify(plain, hashed)


# ─── Token Service ────────────────────────────────────────────────────────────
class TokenService:
    ACCESS_TYPE = "access"
    REFRESH_TYPE = "refresh"

    def create_access_token(
        self,
        subject: str,
        role: str,
        extra_claims: dict[str, Any] | None = None,
    ) -> str:
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
        payload = {
            "sub": subject,
            "role": role,
            "type": self.ACCESS_TYPE,
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid.uuid4()),
            **(extra_claims or {}),
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    def create_refresh_token(self, subject: str, role: str) -> str:
        expires = datetime.now(timezone.utc) + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
        payload = {
            "sub": subject,
            "role": role,
            "type": self.REFRESH_TYPE,
            "exp": expires,
            "iat": datetime.now(timezone.utc),
            "jti": str(uuid.uuid4()),
        }
        return jwt.encode(
            payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
        )

    def decode(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredException()
        except JWTError:
            raise InvalidTokenException()

    def decode_access(self, token: str) -> dict[str, Any]:
        payload = self.decode(token)
        if payload.get("type") != self.ACCESS_TYPE:
            raise InvalidTokenException("Not an access token")
        return payload

    def decode_refresh(self, token: str) -> dict[str, Any]:
        payload = self.decode(token)
        if payload.get("type") != self.REFRESH_TYPE:
            raise InvalidTokenException("Not a refresh token")
        return payload

    def create_token_pair(
        self, subject: str, role: str, extra_claims: dict | None = None
    ) -> tuple[str, str]:
        access = self.create_access_token(subject, role, extra_claims)
        refresh = self.create_refresh_token(subject, role)
        return access, refresh


# Singletons
password_service = PasswordService()
token_service = TokenService()
