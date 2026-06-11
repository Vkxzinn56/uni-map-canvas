"""
UniMap 3.0 - Clinics Domain Models
University health/dental/psychology clinics — no payment processing
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.shared.database.base_entity import BaseEntity


class Clinic(BaseEntity):
    __tablename__ = "clinics"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    clinic_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # dental | medical | psychology | nutrition | physiotherapy | ophthalmology | other
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str | None] = mapped_column(String(200), nullable=True)
    block_code: Mapped[str | None] = mapped_column(String(20), nullable=True)
    room_code: Mapped[str | None] = mapped_column(String(30), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    schedule_info: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    accepts_walk_in: Mapped[bool] = mapped_column(default=False, nullable=False)

    appointments: Mapped[list["ClinicAppointment"]] = relationship(
        "ClinicAppointment", back_populates="clinic", lazy="select"
    )


class ClinicAppointment(BaseEntity):
    __tablename__ = "clinic_appointments"

    clinic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False, index=True
    )
    patient_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )
    scheduled_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    duration_minutes: Mapped[int] = mapped_column(Integer, default=30, nullable=False)

    appointment_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # consultation | return | procedure | evaluation

    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    # Patient's notes/symptoms at booking time

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="scheduled")
    # scheduled | confirmed | cancelled | completed | no_show

    cancellation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    clinic: Mapped["Clinic"] = relationship("Clinic", back_populates="appointments")


class ClinicBudget(BaseEntity):
    """Treatment quote/budget (no payment — information only)."""

    __tablename__ = "clinic_budgets"

    clinic_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clinics.id"), nullable=False
    )
    patient_user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    appointment_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clinic_appointments.id"), nullable=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    procedures: Mapped[str | None] = mapped_column(Text, nullable=True)
    # JSON-serialized list of procedures
    estimated_sessions: Mapped[int | None] = mapped_column(Integer, nullable=True)
    valid_until: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    status: Mapped[str] = mapped_column(String(20), default="pending", nullable=False)
    # pending | accepted | declined | expired
