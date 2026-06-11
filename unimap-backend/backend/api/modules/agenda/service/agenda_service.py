"""
UniMap 3.0 - Agenda Service
"""
import uuid
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.modules.agenda.models.agenda_models import AcademicClass, Activity
from backend.api.modules.students.models.student import Student
from backend.api.modules.users.models.user import User
from backend.shared.exceptions.auth import NotFoundException, BusinessRuleException


class AgendaService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def _get_student(self, user_id: str) -> Student:
        stmt = (
            select(Student)
            .join(User, Student.user_id == User.id)
            .where(User.id == uuid.UUID(user_id), Student.deleted_at.is_(None))
        )
        result = await self._session.execute(stmt)
        student = result.scalar_one_or_none()
        if not student:
            raise NotFoundException("Student profile", user_id)
        return student

    async def get_agenda(
        self,
        user_id: str,
        week_start: date | None = None,
        semester: str | None = None,
    ) -> dict:
        student = await self._get_student(user_id)
        classes = await self.get_classes(user_id=user_id, semester=semester)
        activities = await self.get_activities(user_id=user_id, pending_only=True)

        # Group classes by day
        by_day: dict[int, list] = {i: [] for i in range(7)}
        for cls in classes:
            by_day[cls["day_of_week"]].append(cls)

        return {
            "student_id": str(student.id),
            "semester": semester or student.enrollment_year,
            "week_start": week_start.isoformat() if week_start else None,
            "schedule": by_day,
            "upcoming_activities": activities[:10],
        }

    async def get_classes(
        self,
        user_id: str,
        subject_code: str | None = None,
        day_of_week: int | None = None,
        semester: str | None = None,
    ) -> list[dict]:
        student = await self._get_student(user_id)
        stmt = select(AcademicClass).where(
            AcademicClass.student_id == student.id,
            AcademicClass.deleted_at.is_(None),
        )
        if subject_code:
            stmt = stmt.where(AcademicClass.subject_code == subject_code)
        if day_of_week is not None:
            stmt = stmt.where(AcademicClass.day_of_week == day_of_week)
        if semester:
            stmt = stmt.where(AcademicClass.semester_label == semester)
        stmt = stmt.order_by(AcademicClass.day_of_week, AcademicClass.start_time)
        result = await self._session.execute(stmt)
        classes = result.scalars().all()
        return [
            {
                "id": str(c.id),
                "subject_code": c.subject_code,
                "subject_name": c.subject_name,
                "professor_name": c.professor_name,
                "day_of_week": c.day_of_week,
                "start_time": str(c.start_time),
                "end_time": str(c.end_time),
                "block_code": c.block_code,
                "room_code": c.room_code,
                "class_type": c.class_type,
                "semester_label": c.semester_label,
            }
            for c in classes
        ]

    async def get_activities(
        self,
        user_id: str,
        activity_type: str | None = None,
        pending_only: bool = False,
    ) -> list[dict]:
        student = await self._get_student(user_id)
        stmt = select(Activity).where(
            Activity.student_id == student.id,
            Activity.deleted_at.is_(None),
        )
        if activity_type:
            stmt = stmt.where(Activity.activity_type == activity_type)
        if pending_only:
            stmt = stmt.where(
                Activity.is_completed == False,
                Activity.due_at > datetime.now(timezone.utc),
            )
        stmt = stmt.order_by(Activity.due_at)
        result = await self._session.execute(stmt)
        activities = result.scalars().all()
        return [
            {
                "id": str(a.id),
                "title": a.title,
                "description": a.description,
                "activity_type": a.activity_type,
                "subject_code": a.subject_code,
                "due_at": a.due_at.isoformat(),
                "is_completed": a.is_completed,
                "weight": a.weight,
                "max_score": a.max_score,
                "achieved_score": a.achieved_score,
            }
            for a in activities
        ]

    async def create_activity(self, user_id: str, data: dict) -> dict:
        student = await self._get_student(user_id)
        activity = Activity(
            student_id=student.id,
            title=data["title"],
            description=data.get("description"),
            activity_type=data.get("activity_type", "other"),
            subject_code=data.get("subject_code"),
            due_at=datetime.fromisoformat(data["due_at"]),
            weight=data.get("weight"),
            max_score=data.get("max_score"),
        )
        self._session.add(activity)
        await self._session.flush()
        return {"id": str(activity.id), "title": activity.title}

    async def update_activity(
        self, activity_id: uuid.UUID, user_id: str, data: dict
    ) -> dict:
        student = await self._get_student(user_id)
        stmt = select(Activity).where(
            Activity.id == activity_id,
            Activity.student_id == student.id,
            Activity.deleted_at.is_(None),
        )
        result = await self._session.execute(stmt)
        activity = result.scalar_one_or_none()
        if not activity:
            raise NotFoundException("Activity", str(activity_id))

        for field in ("title", "description", "is_completed", "achieved_score"):
            if field in data:
                setattr(activity, field, data[field])
        await self._session.flush()
        return {"id": str(activity.id), "updated": True}
