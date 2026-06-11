"""
UniMap 3.0 - Agenda Domain Models
STUDENT+ access only — not available to VISITOR
"""
import uuid
from datetime import datetime, time

from sqlalchemy import DateTime, ForeignKey, Integer, String, Time
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity


class AcademicClass(BaseEntity):
    """A single class/lecture occurrence in the schedule."""

    __tablename__ = "academic_classes"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True
    )
    subject_code: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    subject_name: Mapped[str] = mapped_column(String(200), nullable=False)
    professor_name: Mapped[str | None] = mapped_column(String(200), nullable=True)

    # Schedule
    day_of_week: Mapped[int] = mapped_column(Integer, nullable=False)
    # 0=Monday ... 6=Sunday
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)

    # Location
    block_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    room_code: Mapped[str | None] = mapped_column(String(30), nullable=True)

    semester_label: Mapped[str] = mapped_column(String(20), nullable=False)
    # e.g. "2024-1"

    class_type: Mapped[str] = mapped_column(String(20), default="theoretical", nullable=False)
    # theoretical | practical | lab | online


class Activity(BaseEntity):
    """One-off academic activity (test, assignment, deadline)."""

    __tablename__ = "activities"

    student_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("students.id"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(String(300), nullable=False)
    description: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    activity_type: Mapped[str] = mapped_column(String(30), nullable=False)
    # exam | assignment | presentation | project | other
    subject_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    weight: Mapped[float | None] = mapped_column(nullable=True)
    max_score: Mapped[float | None] = mapped_column(nullable=True)
    achieved_score: Mapped[float | None] = mapped_column(nullable=True)
