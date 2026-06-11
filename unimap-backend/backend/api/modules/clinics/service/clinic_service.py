"""
UniMap 3.0 - Clinics Service
"""
import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.clinics.models.clinic_models import (
    Clinic,
    ClinicAppointment,
    ClinicBudget,
)
from backend.shared.exceptions.auth import (
    BusinessRuleException,
    NotFoundException,
)


class ClinicService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_clinics(self, clinic_type: str | None = None) -> list[dict]:
        stmt = select(Clinic).where(Clinic.deleted_at.is_(None), Clinic.is_active == True)
        if clinic_type:
            stmt = stmt.where(Clinic.clinic_type == clinic_type)
        stmt = stmt.order_by(Clinic.name)
        result = await self._session.execute(stmt)
        clinics = result.scalars().all()
        return [self._serialize_clinic(c) for c in clinics]

    async def get_clinic(self, clinic_id: uuid.UUID) -> dict:
        stmt = select(Clinic).where(
            Clinic.id == clinic_id, Clinic.deleted_at.is_(None)
        )
        result = await self._session.execute(stmt)
        clinic = result.scalar_one_or_none()
        if not clinic:
            raise NotFoundException("Clinic", str(clinic_id))
        return self._serialize_clinic(clinic, detail=True)

    async def get_availability(self, clinic_id: uuid.UUID, date_str: str) -> dict:
        """
        Return available slots for a given clinic on a given date.
        TODO: integrate with real scheduling system / Blackboard.
        """
        from datetime import date, timedelta

        target = date.fromisoformat(date_str)
        # Placeholder slots — real implementation should check existing appointments
        slots = []
        for hour in range(8, 18):
            for minute in (0, 30):
                slot_time = f"{hour:02d}:{minute:02d}"
                slots.append({"time": slot_time, "available": True})

        return {
            "clinic_id": str(clinic_id),
            "date": date_str,
            "slots": slots,
        }

    async def book_appointment(self, patient_user_id: str, data: dict) -> dict:
        clinic_id = uuid.UUID(data["clinic_id"])
        scheduled_at = datetime.fromisoformat(data["scheduled_at"])

        # Ensure clinic exists
        await self.get_clinic(clinic_id)

        # Check for double-booking
        conflict_stmt = select(ClinicAppointment).where(
            ClinicAppointment.patient_user_id == uuid.UUID(patient_user_id),
            ClinicAppointment.scheduled_at == scheduled_at,
            ClinicAppointment.status.in_(["scheduled", "confirmed"]),
            ClinicAppointment.deleted_at.is_(None),
        )
        conflict = await self._session.execute(conflict_stmt)
        if conflict.scalar_one_or_none():
            raise BusinessRuleException("You already have an appointment at this time")

        appointment = ClinicAppointment(
            clinic_id=clinic_id,
            patient_user_id=uuid.UUID(patient_user_id),
            scheduled_at=scheduled_at,
            duration_minutes=data.get("duration_minutes", 30),
            appointment_type=data.get("appointment_type", "consultation"),
            notes=data.get("notes"),
            status="scheduled",
        )
        self._session.add(appointment)
        await self._session.flush()
        return {"id": str(appointment.id), "status": appointment.status}

    async def get_patient_appointments(
        self,
        patient_user_id: str,
        status_filter: str | None = None,
        include_past: bool = False,
    ) -> list[dict]:
        stmt = select(ClinicAppointment).where(
            ClinicAppointment.patient_user_id == uuid.UUID(patient_user_id),
            ClinicAppointment.deleted_at.is_(None),
        )
        if status_filter:
            stmt = stmt.where(ClinicAppointment.status == status_filter)
        if not include_past:
            stmt = stmt.where(
                ClinicAppointment.scheduled_at >= datetime.now(timezone.utc)
            )
        stmt = stmt.order_by(ClinicAppointment.scheduled_at)
        result = await self._session.execute(stmt)
        appts = result.scalars().all()
        return [
            {
                "id": str(a.id),
                "clinic_id": str(a.clinic_id),
                "scheduled_at": a.scheduled_at.isoformat(),
                "appointment_type": a.appointment_type,
                "status": a.status,
                "duration_minutes": a.duration_minutes,
            }
            for a in appts
        ]

    async def cancel_appointment(
        self,
        appointment_id: uuid.UUID,
        patient_user_id: str,
        reason: str | None = None,
    ) -> None:
        stmt = select(ClinicAppointment).where(
            ClinicAppointment.id == appointment_id,
            ClinicAppointment.patient_user_id == uuid.UUID(patient_user_id),
            ClinicAppointment.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        appt = result.scalar_one_or_none()
        if not appt:
            raise NotFoundException("Appointment", str(appointment_id))
        if appt.status in ("completed", "cancelled"):
            raise BusinessRuleException(f"Cannot cancel a {appt.status} appointment")
        appt.status = "cancelled"
        appt.cancellation_reason = reason
        await self._session.flush()

    async def get_patient_budgets(self, patient_user_id: str) -> list[dict]:
        stmt = select(ClinicBudget).where(
            ClinicBudget.patient_user_id == uuid.UUID(patient_user_id),
            ClinicBudget.deleted_at.is_(None),
        ).order_by(ClinicBudget.created_at.desc())
        result = await self._session.execute(stmt)
        budgets = result.scalars().all()
        return [
            {
                "id": str(b.id),
                "clinic_id": str(b.clinic_id),
                "description": b.description,
                "estimated_sessions": b.estimated_sessions,
                "status": b.status,
                "valid_until": b.valid_until.isoformat() if b.valid_until else None,
            }
            for b in budgets
        ]

    def _serialize_clinic(self, clinic: Clinic, detail: bool = False) -> dict:
        base = {
            "id": str(clinic.id),
            "name": clinic.name,
            "clinic_type": clinic.clinic_type,
            "location": clinic.location,
            "block_code": clinic.block_code,
            "accepts_walk_in": clinic.accepts_walk_in,
            "image_url": clinic.image_url,
        }
        if detail:
            base["description"] = clinic.description
            base["phone"] = clinic.phone
            base["email"] = clinic.email
            base["schedule_info"] = clinic.schedule_info
            base["room_code"] = clinic.room_code
        return base
