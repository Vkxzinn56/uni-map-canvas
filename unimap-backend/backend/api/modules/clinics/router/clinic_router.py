"""
UniMap 3.0 - Clinics Router
GET /clinics → VISITOR+
POST /clinics/appointments → STUDENT+
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.clinics.service.clinic_service import ClinicService
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import (
    AcademicOnly,
    CurrentUser,
    UserRole,
    get_current_user,
    get_optional_user,
    require_roles,
)

router = APIRouter(prefix="/clinics", tags=["Clinics"])


def get_clinic_service(session: AsyncSession = Depends(get_db)) -> ClinicService:
    return ClinicService(session)


@router.get("", summary="List all university clinics — public")
async def list_clinics(
    clinic_type: str | None = Query(None, description="Filter by type"),
    service: ClinicService = Depends(get_clinic_service),
) -> list[dict]:
    return await service.list_clinics(clinic_type=clinic_type)


@router.get("/{clinic_id}", summary="Get clinic details — public")
async def get_clinic(
    clinic_id: uuid.UUID,
    service: ClinicService = Depends(get_clinic_service),
) -> dict:
    return await service.get_clinic(clinic_id)


@router.get(
    "/{clinic_id}/availability",
    summary="Check available slots — public",
)
async def get_availability(
    clinic_id: uuid.UUID,
    date: str = Query(..., description="ISO date YYYY-MM-DD"),
    service: ClinicService = Depends(get_clinic_service),
) -> dict:
    return await service.get_availability(clinic_id, date)


# ─── Appointment (STUDENT+) ───────────────────────────────────────────────────

@router.post(
    "/appointments",
    status_code=status.HTTP_201_CREATED,
    summary="Book an appointment — STUDENT+",
    dependencies=[AcademicOnly],
)
async def book_appointment(
    body: dict,
    current_user: CurrentUser = Depends(get_current_user),
    service: ClinicService = Depends(get_clinic_service),
) -> dict:
    return await service.book_appointment(
        patient_user_id=current_user.user_id, data=body
    )


@router.get(
    "/appointments/me",
    summary="My appointments — STUDENT+",
    dependencies=[AcademicOnly],
)
async def my_appointments(
    status_filter: str | None = Query(None),
    current_user: CurrentUser = Depends(get_current_user),
    service: ClinicService = Depends(get_clinic_service),
) -> list[dict]:
    return await service.get_patient_appointments(
        patient_user_id=current_user.user_id, status_filter=status_filter
    )


@router.delete(
    "/appointments/{appointment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Cancel appointment — STUDENT+",
    dependencies=[AcademicOnly],
)
async def cancel_appointment(
    appointment_id: uuid.UUID,
    body: dict | None = None,
    current_user: CurrentUser = Depends(get_current_user),
    service: ClinicService = Depends(get_clinic_service),
) -> None:
    await service.cancel_appointment(
        appointment_id=appointment_id,
        patient_user_id=current_user.user_id,
        reason=(body or {}).get("reason"),
    )


@router.get(
    "/appointments/me/history",
    summary="Appointment history — STUDENT+",
    dependencies=[AcademicOnly],
)
async def appointment_history(
    current_user: CurrentUser = Depends(get_current_user),
    service: ClinicService = Depends(get_clinic_service),
) -> list[dict]:
    return await service.get_patient_appointments(
        patient_user_id=current_user.user_id, include_past=True
    )


# ─── Budget ───────────────────────────────────────────────────────────────────

@router.get(
    "/budgets/me",
    summary="My treatment budgets — STUDENT+",
    dependencies=[AcademicOnly],
)
async def my_budgets(
    current_user: CurrentUser = Depends(get_current_user),
    service: ClinicService = Depends(get_clinic_service),
) -> list[dict]:
    return await service.get_patient_budgets(patient_user_id=current_user.user_id)
