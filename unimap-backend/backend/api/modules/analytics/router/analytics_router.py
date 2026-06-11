"""
UniMap 3.0 - Analytics Router
Admin/Coordinator: platform usage metrics
"""
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.users.models.user import User
from backend.api.modules.events.models.event import Event
from backend.api.modules.clinics.models.clinic_models import ClinicAppointment
from backend.api.modules.notifications.models.notification import Notification
from backend.shared.database.engine import get_db
from backend.shared.security.rbac import StaffOnly, get_current_user, CurrentUser

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get(
    "/overview",
    dependencies=[StaffOnly],
    summary="Platform overview metrics",
)
async def overview(
    session: AsyncSession = Depends(get_db),
) -> dict:
    """Dashboard-level stats for coordinators and admins."""

    # User counts by role
    role_stmt = select(User.role, func.count(User.id)).where(
        User.deleted_at.is_(None)
    ).group_by(User.role)
    role_result = await session.execute(role_stmt)
    users_by_role = {row[0]: row[1] for row in role_result.all()}

    # Total active users
    total_users = sum(users_by_role.values())

    # Events this month
    events_stmt = select(func.count(Event.id)).where(
        Event.deleted_at.is_(None),
        Event.status == "published",
    )
    events_result = await session.execute(events_stmt)
    total_events = events_result.scalar_one()

    # Appointments this month
    appt_stmt = select(func.count(ClinicAppointment.id)).where(
        ClinicAppointment.deleted_at.is_(None),
        ClinicAppointment.status.in_(["scheduled", "confirmed", "completed"]),
    )
    appt_result = await session.execute(appt_stmt)
    total_appointments = appt_result.scalar_one()

    return {
        "total_users": total_users,
        "users_by_role": users_by_role,
        "total_events": total_events,
        "total_appointments": total_appointments,
    }


@router.get(
    "/users/growth",
    dependencies=[StaffOnly],
    summary="User registration growth over time",
)
async def user_growth(
    months: int = Query(6, ge=1, le=24),
    session: AsyncSession = Depends(get_db),
) -> list[dict]:
    stmt = text(
        """
        SELECT
            TO_CHAR(DATE_TRUNC('month', created_at), 'YYYY-MM') AS month,
            COUNT(*) AS new_users
        FROM users
        WHERE deleted_at IS NULL
          AND created_at >= NOW() - INTERVAL ':months months'
        GROUP BY 1
        ORDER BY 1
        """
    ).bindparams(months=months)
    result = await session.execute(stmt)
    return [{"month": row[0], "new_users": row[1]} for row in result.all()]


@router.get(
    "/clinics/utilization",
    dependencies=[StaffOnly],
    summary="Clinic appointment utilization",
)
async def clinic_utilization(
    session: AsyncSession = Depends(get_db),
) -> list[dict]:
    from backend.api.modules.clinics.models.clinic_models import Clinic

    stmt = (
        select(
            Clinic.name,
            Clinic.clinic_type,
            func.count(ClinicAppointment.id).label("total"),
        )
        .join(ClinicAppointment, Clinic.id == ClinicAppointment.clinic_id, isouter=True)
        .where(Clinic.deleted_at.is_(None))
        .group_by(Clinic.id, Clinic.name, Clinic.clinic_type)
        .order_by(func.count(ClinicAppointment.id).desc())
    )
    result = await session.execute(stmt)
    return [
        {"clinic": row[0], "type": row[1], "appointments": row[2]}
        for row in result.all()
    ]


@router.get(
    "/map/popular-blocks",
    dependencies=[StaffOnly],
    summary="Most accessed map blocks",
)
async def popular_blocks(
    session: AsyncSession = Depends(get_db),
) -> list[dict]:
    """
    Returns top blocks based on audit log reads.
    Future: integrate with map click/navigation events.
    """
    from backend.api.modules.audit.models.audit_log import AuditLog

    stmt = (
        select(AuditLog.resource_id, func.count(AuditLog.id).label("views"))
        .where(
            AuditLog.resource_type == "Block",
            AuditLog.action == "READ",
        )
        .group_by(AuditLog.resource_id)
        .order_by(func.count(AuditLog.id).desc())
        .limit(10)
    )
    result = await session.execute(stmt)
    return [{"block_id": row[0], "views": row[1]} for row in result.all()]
