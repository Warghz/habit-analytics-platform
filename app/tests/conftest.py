from unittest.mock import AsyncMock, patch
import pytest
from datetime import date
from app.repositories.habits import HabitRepository
from app.services.habit_log import HabitLogService
from app.repositories.habit_log import HabitLogRepository
from app.api.main import app


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def habit():
    return type("habit", (), {
        "id": 1,
        "name": "test"
    })()


@pytest.fixture
def mock_habit_exists():
    HabitRepository.get_habits_by_id = AsyncMock(return_value=habit)
    return habit


@pytest.fixture
def mock_no_habit():
    HabitRepository.get_habits_by_id = AsyncMock(return_value=None)


@pytest.fixture
def mock_already_done():
    HabitLogRepository.exists_today = AsyncMock(return_value=True)


@pytest.fixture
def mock_already_not_done():
    HabitLogRepository.exists_today = AsyncMock(return_value=False)


@pytest.fixture
def mock_empty_dates():
    HabitLogRepository.get_completion_dates = AsyncMock(return_value=[])


@pytest.fixture
def mock_one_day():
    HabitLogRepository.get_completion_dates = AsyncMock(return_value=[date.today()])


@pytest.fixture
def mock_create_log():
    HabitLogRepository.create_log = AsyncMock(return_value={"log_id": 10})


@pytest.fixture
def mock_update_habit():
    habit = AsyncMock()
    result = HabitRepository.get_habits_by_id(None, 1, 1)
    return result

