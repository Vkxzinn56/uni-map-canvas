"""
UniMap 3.0 - User Domain Model
DDD: Aggregate Root — represents any platform user
Sensitive fields encrypted with AES-256
"""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, Enum, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity
from backend.shared.security.rbac import UserRole


class User(BaseEntity):
    __tablename__ = "users"

    # ── Identity ──────────────────────────────────────────────────────────────
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    hashed_password: Mapped[str] = mapped_column(Text, nullable=False)

    # ── Profile ───────────────────────────────────────────────────────────────
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    display_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── RBAC ──────────────────────────────────────────────────────────────────
    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=UserRole.VISITOR.value,
        index=True,
    )

    # ── Encrypted Sensitive Data (AES-256) ────────────────────────────────────
    # These columns store AES-256-GCM encrypted values
    cpf_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)
    cpf_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True, unique=True, index=True
    )  # SHA-256 hash for lookup only

    address_encrypted: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Status ────────────────────────────────────────────────────────────────
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    block_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── LGPD ──────────────────────────────────────────────────────────────────
    lgpd_consent_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    lgpd_consent_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    anonymized_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Security ──────────────────────────────────────────────────────────────
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    last_login_ip: Mapped[str | None] = mapped_column(String(45), nullable=True)
    failed_login_attempts: Mapped[int] = mapped_column(default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # ── Relationships ─────────────────────────────────────────────────────────
    student_profile: Mapped["Student | None"] = relationship(
        "Student", back_populates="user", uselist=False, lazy="select"
    )

    @property
    def user_role(self) -> UserRole:
        return UserRole(self.role)

    @property
    def is_alumni(self) -> bool:
        return self.role == UserRole.ALUMNI.value

    @property
    def is_student(self) -> bool:
        return self.role == UserRole.STUDENT.value

    def block(self, reason: str) -> None:
        self.is_blocked = True
        self.block_reason = reason

    def unblock(self) -> None:
        self.is_blocked = False
        self.block_reason = None
        self.failed_login_attempts = 0
        self.locked_until = None
