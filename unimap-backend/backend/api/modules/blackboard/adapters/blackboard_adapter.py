"""
UniMap 3.0 - Blackboard Adapter
Integration: Blackboard LMS adapter (PREPARED — NOT ACTIVE)

This file prepares the interface for future Blackboard integration.
No implementation is active. Set BLACKBOARD_ENABLED=true to activate.

Blackboard REST API Reference:
https://developer.blackboard.com/portal/displayApi
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class BlackboardUser:
    id: str
    username: str
    email: str
    given_name: str
    family_name: str
    student_id: str | None = None
    availability: str = "Yes"


@dataclass
class BlackboardCourse:
    id: str
    course_id: str
    name: str
    description: str | None
    term: str | None
    instructor: str | None
    enrollment_status: str


@dataclass
class BlackboardGrade:
    column_id: str
    column_name: str
    score: float | None
    max_score: float
    attempt_date: datetime | None
    status: str  # Graded | NotAttempted | InProgress


@dataclass
class BlackboardAnnouncement:
    id: str
    title: str
    body: str
    posted_at: datetime
    course_id: str


class IBlackboardAdapter(ABC):
    """
    Port (interface) for Blackboard integration.
    Implement this interface with a concrete adapter when integration is ready.
    """

    @abstractmethod
    async def get_user_by_username(self, username: str) -> BlackboardUser | None:
        """Fetch a Blackboard user by their username."""
        ...

    @abstractmethod
    async def get_user_courses(self, user_id: str) -> list[BlackboardCourse]:
        """Return all courses enrolled by a user."""
        ...

    @abstractmethod
    async def get_course_grades(
        self, course_id: str, user_id: str
    ) -> list[BlackboardGrade]:
        """Return grade data for a user in a given course."""
        ...

    @abstractmethod
    async def get_course_announcements(
        self, course_id: str
    ) -> list[BlackboardAnnouncement]:
        """Return announcements for a course."""
        ...

    @abstractmethod
    async def sync_user_schedule(self, user_id: str) -> list[dict]:
        """Sync and return user's class schedule from Blackboard."""
        ...

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify Blackboard API is reachable and credentials are valid."""
        ...


class BlackboardNotEnabledAdapter(IBlackboardAdapter):
    """
    Stub adapter that raises clear errors when Blackboard is disabled.
    Used as default when BLACKBOARD_ENABLED=false.
    """

    _ERROR = "Blackboard integration is not enabled. Set BLACKBOARD_ENABLED=true."

    async def get_user_by_username(self, username: str) -> BlackboardUser | None:
        raise NotImplementedError(self._ERROR)

    async def get_user_courses(self, user_id: str) -> list[BlackboardCourse]:
        raise NotImplementedError(self._ERROR)

    async def get_course_grades(
        self, course_id: str, user_id: str
    ) -> list[BlackboardGrade]:
        raise NotImplementedError(self._ERROR)

    async def get_course_announcements(
        self, course_id: str
    ) -> list[BlackboardAnnouncement]:
        raise NotImplementedError(self._ERROR)

    async def sync_user_schedule(self, user_id: str) -> list[dict]:
        raise NotImplementedError(self._ERROR)

    async def health_check(self) -> bool:
        return False
