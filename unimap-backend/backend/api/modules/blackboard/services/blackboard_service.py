"""
UniMap 3.0 - Blackboard Service
Integration: Orchestrates Blackboard data into UniMap domain objects

PREPARED — NOT ACTIVE. Activate with BLACKBOARD_ENABLED=true

When enabled:
- Syncs student schedule from Blackboard → AcademicClass table
- Pushes notifications for announcements
- Exposes grade data (read-only)
"""
from backend.api.modules.blackboard.adapters.blackboard_adapter import (
    BlackboardAnnouncement,
    BlackboardCourse,
    BlackboardGrade,
    BlackboardNotEnabledAdapter,
    BlackboardUser,
    IBlackboardAdapter,
)
from backend.core.config.settings import settings


class BlackboardService:
    """
    High-level Blackboard integration service.
    Uses the IBlackboardAdapter port — swap implementation without changing this class.
    """

    def __init__(self) -> None:
        self._adapter: IBlackboardAdapter = self._resolve_adapter()

    def _resolve_adapter(self) -> IBlackboardAdapter:
        if not settings.BLACKBOARD_ENABLED:
            return BlackboardNotEnabledAdapter()
        # When real adapter is implemented, import and return it here:
        # from backend.api.modules.blackboard.adapters.real_adapter import RealBlackboardAdapter
        # return RealBlackboardAdapter(BlackboardProvider())
        return BlackboardNotEnabledAdapter()

    async def is_available(self) -> bool:
        """Check if Blackboard integration is active and healthy."""
        if not settings.BLACKBOARD_ENABLED:
            return False
        return await self._adapter.health_check()

    async def get_student_courses(self, blackboard_username: str) -> list[BlackboardCourse]:
        """
        Return all Blackboard courses for a student.
        Raises NotImplementedError if integration is disabled.
        """
        user = await self._adapter.get_user_by_username(blackboard_username)
        if not user:
            return []
        return await self._adapter.get_user_courses(user.id)

    async def get_grades_for_course(
        self, blackboard_user_id: str, course_id: str
    ) -> list[BlackboardGrade]:
        return await self._adapter.get_course_grades(course_id, blackboard_user_id)

    async def sync_schedule_to_unimap(
        self, unimap_student_id: str, blackboard_username: str
    ) -> dict:
        """
        Pull schedule from Blackboard and upsert into UniMap's AcademicClass table.
        Returns summary of synced items.

        TODO: Implement when BLACKBOARD_ENABLED=true and adapter is wired.
        """
        raw_schedule = await self._adapter.sync_user_schedule(blackboard_username)
        # Map Blackboard schedule → AcademicClass domain objects
        # This method is a placeholder for the full sync logic
        return {
            "synced": len(raw_schedule),
            "source": "blackboard",
            "status": "prepared",
        }

    async def get_announcements(self, course_id: str) -> list[BlackboardAnnouncement]:
        return await self._adapter.get_course_announcements(course_id)


# Module-level singleton
blackboard_service = BlackboardService()
