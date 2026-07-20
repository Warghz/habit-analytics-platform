from datetime import date
from unittest.mock import AsyncMock

import pytest

from app.core.exceptions import HabitNotFoundError
from app.repositories.habit_log import HabitLogRepository
from app.repositories.habits import HabitRepository
from app.services.habit_analytics import HabitAnalyticsService


class FakeHabit:
    id = 10
    name = "reading"


class FakeLog:
    def __init__(self, completed_date):
        self.completed_date = completed_date


@pytest.mark.asyncio
async def test_get_habit_stats_passes_user_id_to_logs_repository(monkeypatch):
    get_habit = AsyncMock(return_value=FakeHabit())
    get_logs = AsyncMock(return_value=[FakeLog(date.today())])

    monkeypatch.setattr(HabitRepository, "get_habits_by_id", get_habit)
    monkeypatch.setattr(HabitLogRepository, "get_logs", get_logs)

    result = await HabitAnalyticsService.get_habit_stats(
        session="session",
        habit_id=10,
        user_id=77,
    )

    get_habit.assert_awaited_once_with("session", 10, 77)
    get_logs.assert_awaited_once_with("session", 10, 77)
    assert result["habit_name"] == "reading"
    assert result["total_completions"] == 1


@pytest.mark.asyncio
async def test_get_habit_stats_raises_when_habit_not_found(monkeypatch):
    monkeypatch.setattr(
        HabitRepository,
        "get_habits_by_id",
        AsyncMock(return_value=None)
    )

    with pytest.raises(HabitNotFoundError):
        await HabitAnalyticsService.get_habit_stats(
            session="session",
            habit_id=10,
            user_id=77,
        )
