"""
UniMap 3.0 - Student Domain Model
DDD: Entity — extends User with academic data
RGM encrypted with AES-256
"""
import uuid
from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity


class Student(BaseEntity):
    __tablename__ = "students"

    # ── User FK ───────────────────────────────────────────────────────────────
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="RESTRICT"),
        unique=True,
        nullable=False,
        index=True,
    )

    # ── Academic Identifiers (Encrypted) ──────────────────────────────────────
    rgm_encrypted: Mapped[str] = mapped_column(Text, nullable=False)
    rgm_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True
    )

    # ── Academic Info ─────────────────────────────────────────────────────────
    course: Mapped[str] = mapped_column(String(200), nullable=False)
    course_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    semester: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    enrollment_year: Mapped[int] = mapped_column(Integer, nullable=False)
    expected_graduation: Mapped[date | None] = mapped_column(Date, nullable=True)
    graduation_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # ── Campus ────────────────────────────────────────────────────────────────
    campus: Mapped[str] = mapped_column(String(100), nullable=False)
    campus_code: Mapped[str | None] = mapped_column(String(10), nullable=True)
    period: Mapped[str] = mapped_column(
        String(10), nullable=False, default="morning"
    )  # morning | afternoon | evening

    # ── Status ────────────────────────────────────────────────────────────────
    enrollment_status: Mapped[str] = mapped_column(
        String(30), nullable=False, default="active"
    )
    # active | suspended | graduated | cancelled | transferred

    # ── Relationships ─────────────────────────────────────────────────────────
    user: Mapped["User"] = relationship(
        "User", back_populates="student_profile", lazy="select"
    )

    @property
    def is_graduated(self) -> bool:
        return self.enrollment_status == "graduated"

    @property
    def is_active_student(self) -> bool:
        return self.enrollment_status == "active"
