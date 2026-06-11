"""
UniMap 3.0 - Blackboard Tests
Verifies the prepared (non-active) integration stubs
"""
import pytest

from backend.api.modules.blackboard.adapters.blackboard_adapter import (
    BlackboardNotEnabledAdapter,
    IBlackboardAdapter,
)
from backend.api.modules.blackboard.services.blackboard_service import BlackboardService


class TestBlackboardNotEnabled:
    """All operations raise NotImplementedError when disabled."""

    def setup_method(self):
        self.adapter = BlackboardNotEnabledAdapter()

    @pytest.mark.asyncio
    async def test_health_check_returns_false(self):
        result = await self.adapter.health_check()
        assert result is False

    @pytest.mark.asyncio
    async def test_get_user_raises(self):
        with pytest.raises(NotImplementedError) as exc:
            await self.adapter.get_user_by_username("testuser")
        assert "not enabled" in str(exc.value).lower()

    @pytest.mark.asyncio
    async def test_get_courses_raises(self):
        with pytest.raises(NotImplementedError):
            await self.adapter.get_user_courses("user_id")

    @pytest.mark.asyncio
    async def test_get_grades_raises(self):
        with pytest.raises(NotImplementedError):
            await self.adapter.get_course_grades("course_id", "user_id")

    @pytest.mark.asyncio
    async def test_announcements_raises(self):
        with pytest.raises(NotImplementedError):
            await self.adapter.get_course_announcements("course_id")


class TestBlackboardService:
    def setup_method(self):
        self.service = BlackboardService()

    @pytest.mark.asyncio
    async def test_is_available_false_when_disabled(self):
        result = await self.service.is_available()
        assert result is False

    @pytest.mark.asyncio
    async def test_service_uses_stub_adapter(self):
        assert isinstance(self.service._adapter, BlackboardNotEnabledAdapter)

    def test_adapter_implements_interface(self):
        adapter = BlackboardNotEnabledAdapter()
        assert isinstance(adapter, IBlackboardAdapter)
