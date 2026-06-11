"""
UniMap 3.0 - Custom Exceptions
Clean Architecture: Domain + Application exceptions
"""
from fastapi import HTTPException, status


# ─── Base ─────────────────────────────────────────────────────────────────────
class UniMapException(Exception):
    """Base for all UniMap domain exceptions."""

    def __init__(self, message: str = "An error occurred", code: str = "UNIMAP_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


# ─── Auth Exceptions ──────────────────────────────────────────────────────────
class AuthException(UniMapException):
    pass


class InvalidTokenException(AuthException):
    def __init__(self, detail: str = "Invalid or missing token"):
        super().__init__(detail, "INVALID_TOKEN")


class TokenExpiredException(AuthException):
    def __init__(self):
        super().__init__("Token has expired", "TOKEN_EXPIRED")


class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__("Invalid email or password", "INVALID_CREDENTIALS")


class InsufficientPermissionsException(AuthException):
    def __init__(self, resource: str = ""):
        super().__init__(
            f"Insufficient permissions{f' for {resource}' if resource else ''}",
            "INSUFFICIENT_PERMISSIONS",
        )


class AccountBlockedException(AuthException):
    def __init__(self, reason: str = "Account is blocked"):
        super().__init__(reason, "ACCOUNT_BLOCKED")


# ─── Domain Exceptions ────────────────────────────────────────────────────────
class NotFoundException(UniMapException):
    def __init__(self, resource: str, identifier: str = ""):
        super().__init__(
            f"{resource}{f' [{identifier}]' if identifier else ''} not found",
            "NOT_FOUND",
        )


class AlreadyExistsException(UniMapException):
    def __init__(self, resource: str, field: str = ""):
        super().__init__(
            f"{resource}{f' with {field}' if field else ''} already exists",
            "ALREADY_EXISTS",
        )


class ValidationException(UniMapException):
    def __init__(self, detail: str):
        super().__init__(detail, "VALIDATION_ERROR")


class BusinessRuleException(UniMapException):
    def __init__(self, rule: str):
        super().__init__(rule, "BUSINESS_RULE_VIOLATION")


# ─── HTTP Exception Mappers ───────────────────────────────────────────────────
EXCEPTION_MAP: dict[type[UniMapException], int] = {
    InvalidTokenException: status.HTTP_401_UNAUTHORIZED,
    TokenExpiredException: status.HTTP_401_UNAUTHORIZED,
    InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
    InsufficientPermissionsException: status.HTTP_403_FORBIDDEN,
    AccountBlockedException: status.HTTP_403_FORBIDDEN,
    NotFoundException: status.HTTP_404_NOT_FOUND,
    AlreadyExistsException: status.HTTP_409_CONFLICT,
    ValidationException: status.HTTP_422_UNPROCESSABLE_ENTITY,
    BusinessRuleException: status.HTTP_422_UNPROCESSABLE_ENTITY,
}
