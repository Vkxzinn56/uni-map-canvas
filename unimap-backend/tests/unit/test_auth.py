"""
UniMap 3.0 - Auth Tests
Unit tests for auth service and JWT security
"""
import uuid
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.api.modules.auth.schemas.auth_schemas import LoginRequest, RegisterRequest
from backend.api.modules.users.models.user import User
from backend.shared.exceptions.auth import (
    AccountBlockedException,
    AlreadyExistsException,
    InvalidCredentialsException,
    TokenExpiredException,
)
from backend.shared.security.jwt import password_service, token_service
from backend.shared.security.rbac import UserRole


# ══════════════════════════════════════════════════════════
# JWT Token Tests
# ══════════════════════════════════════════════════════════
class TestTokenService:
    def test_create_access_token(self):
        user_id = str(uuid.uuid4())
        token = token_service.create_access_token(user_id, UserRole.STUDENT.value)
        assert isinstance(token, str)
        assert len(token) > 10

    def test_decode_access_token(self):
        user_id = str(uuid.uuid4())
        token = token_service.create_access_token(user_id, UserRole.ADMIN.value)
        payload = token_service.decode_access(token)
        assert payload["sub"] == user_id
        assert payload["role"] == UserRole.ADMIN.value
        assert payload["type"] == "access"

    def test_create_refresh_token(self):
        user_id = str(uuid.uuid4())
        token = token_service.create_refresh_token(user_id, UserRole.STUDENT.value)
        payload = token_service.decode_refresh(token)
        assert payload["sub"] == user_id
        assert payload["type"] == "refresh"

    def test_decode_wrong_token_type_raises(self):
        user_id = str(uuid.uuid4())
        refresh = token_service.create_refresh_token(user_id, UserRole.STUDENT.value)
        with pytest.raises(Exception):
            token_service.decode_access(refresh)  # Should fail — it's a refresh token

    def test_create_token_pair(self):
        user_id = str(uuid.uuid4())
        access, refresh = token_service.create_token_pair(user_id, UserRole.VISITOR.value)
        assert access != refresh
        p1 = token_service.decode_access(access)
        p2 = token_service.decode_refresh(refresh)
        assert p1["sub"] == p2["sub"] == user_id

    def test_invalid_token_raises(self):
        with pytest.raises(Exception):
            token_service.decode("not-a-valid-token")

    def test_expired_token_raises(self):
        """Simulate an expired token by manipulating expiry."""
        from datetime import timedelta, timezone, datetime
        from jose import jwt
        from backend.core.config.settings import settings

        payload = {
            "sub": str(uuid.uuid4()),
            "role": "student",
            "type": "access",
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            "jti": str(uuid.uuid4()),
        }
        expired_token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
        with pytest.raises(TokenExpiredException):
            token_service.decode(expired_token)


# ══════════════════════════════════════════════════════════
# Password Tests
# ══════════════════════════════════════════════════════════
class TestPasswordService:
    def test_hash_and_verify(self):
        password = "SecurePass123!"
        hashed = password_service.hash(password)
        assert hashed != password
        assert password_service.verify(password, hashed)

    def test_wrong_password_fails(self):
        hashed = password_service.hash("CorrectPass123!")
        assert not password_service.verify("WrongPass123!", hashed)

    def test_different_hashes_same_password(self):
        """Argon2 uses random salt — same password produces different hashes."""
        h1 = password_service.hash("SamePass123!")
        h2 = password_service.hash("SamePass123!")
        assert h1 != h2  # Different salts


# ══════════════════════════════════════════════════════════
# RBAC Tests
# ══════════════════════════════════════════════════════════
class TestRBAC:
    def test_admin_has_all_permissions(self):
        from backend.shared.security.rbac import has_permission
        assert has_permission(UserRole.ADMIN, "map:read")
        assert has_permission(UserRole.ADMIN, "clinics:write")
        assert has_permission(UserRole.ADMIN, "academic:read")
        assert has_permission(UserRole.ADMIN, "any:random")

    def test_visitor_cannot_access_agenda(self):
        from backend.shared.security.rbac import has_permission
        assert not has_permission(UserRole.VISITOR, "agenda:read")
        assert not has_permission(UserRole.VISITOR, "academic:read")

    def test_visitor_can_access_public(self):
        from backend.shared.security.rbac import has_permission
        assert has_permission(UserRole.VISITOR, "map:read")
        assert has_permission(UserRole.VISITOR, "clinics:read")
        assert has_permission(UserRole.VISITOR, "events:read")

    def test_student_can_access_agenda(self):
        from backend.shared.security.rbac import has_permission
        assert has_permission(UserRole.STUDENT, "agenda:read")
        assert has_permission(UserRole.STUDENT, "classes:read")
        assert has_permission(UserRole.STUDENT, "clinics:write")

    def test_alumni_no_academic_write(self):
        from backend.shared.security.rbac import has_permission
        assert not has_permission(UserRole.ALUMNI, "agenda:read")
        assert has_permission(UserRole.ALUMNI, "map:read")
        assert has_permission(UserRole.ALUMNI, "history:read")


# ══════════════════════════════════════════════════════════
# Auth Schema Validation Tests
# ══════════════════════════════════════════════════════════
class TestAuthSchemas:
    def test_valid_registration(self):
        data = RegisterRequest(
            email="test@unimap.edu.br",
            password="SecurePass123!",
            full_name="Test User",
            lgpd_consent=True,
        )
        assert data.email == "test@unimap.edu.br"

    def test_registration_requires_lgpd_consent(self):
        with pytest.raises(Exception):
            RegisterRequest(
                email="test@unimap.edu.br",
                password="SecurePass123!",
                full_name="Test User",
                lgpd_consent=False,
            )

    def test_weak_password_rejected(self):
        """No uppercase, digit, or special char."""
        with pytest.raises(Exception):
            RegisterRequest(
                email="test@test.com",
                password="weakpassword",
                full_name="Test",
                lgpd_consent=True,
            )

    def test_short_password_rejected(self):
        with pytest.raises(Exception):
            RegisterRequest(
                email="test@test.com",
                password="Ab1!",
                full_name="Test",
                lgpd_consent=True,
            )
