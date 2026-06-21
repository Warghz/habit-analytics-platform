from unittest.mock import AsyncMock
import pytest
import pytest_asyncio

from app.models.habits import Habit
from app.repositories.habits import HabitRepository
from app.repositories.habit_log import HabitLogRepository

habit_stub = type(
    "Habit",
    (),
    {
        "id": 1,
        "name": "test",
        "user_id": 1
    }
)()


@pytest_asyncio.fixture
async def habit(db_session, user):
    habit = Habit(
        user_id=user.id,
        name="test",
        content="test",
        rating=5,
        must_have=False,
    )

    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)
    return habit


@pytest.fixture
def mock_habit_exists(monkeypatch):
    mock = AsyncMock(return_value=habit_stub)
    monkeypatch.setattr(HabitRepository, "get_habits_by_id", mock)
    return habit_stub


@pytest.fixture
def mock_no_habit(monkeypatch):
    monkeypatch.setattr(
        HabitRepository,
        "get_habits_by_id",
        AsyncMock(return_value=None)
    )


@pytest.fixture
def mock_already_done(monkeypatch):
    monkeypatch.setattr(
        HabitLogRepository,
        "exists_today",
        AsyncMock(return_value=True)
    )


@pytest.fixture
def mock_already_not_done(monkeypatch):
    monkeypatch.setattr(
        HabitLogRepository,
        "exists_today",
        AsyncMock(return_value=False)
    )


@pytest.fixture
def mock_create_log(monkeypatch):
    mock = AsyncMock(return_value={"log_id": 10})
    monkeypatch.setattr(HabitLogRepository, "create_log", mock)
    return mock
