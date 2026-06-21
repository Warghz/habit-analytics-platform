from unittest.mock import AsyncMock, Mock
import pytest
from psycopg import IntegrityError

from app.repositories.habits import HabitRepository
from app.services.habits import HabitService
from app.core.exceptions import HabitNotFoundError
from app.schemas.habits import HabitUpdate


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'repo_result, expected_len',
    [
        # no habits
        ([], 0),

        # several habits
        ([1, 2, 3], 3)
    ]
)
async def test_get_all_habits(
        monkeypatch,
        repo_result,
        expected_len
):
    monkeypatch.setattr(
        HabitRepository,
        "get_all_habits",
        AsyncMock(return_value=repo_result)
    )

    result = await HabitService.get_all_habits(None, 1)

    assert len(result) == expected_len


@pytest.mark.asyncio
async def test_not_get_habit_by_id(mock_no_habit):

    with pytest.raises(HabitNotFoundError):
        await HabitService.get_habits_by_id(
            None, 1, 1
        )


@pytest.mark.asyncio
async def test_success_get_habit_by_id(mock_habit_exists):

    result = await HabitService.get_habits_by_id(
        None, 1, 1
    )

    assert result == mock_habit_exists


@pytest.mark.asyncio
async def test_not_delete_habit_by_id(mock_no_habit):

    with pytest.raises(HabitNotFoundError):
        await HabitService.delete_habits(
            None, 1, 1
        )


@pytest.mark.asyncio
async def test_success_delete_habit(monkeypatch, mock_habit_exists):

    delete_mock = AsyncMock(return_value=True)
    monkeypatch.setattr(HabitRepository, "delete", delete_mock)

    await HabitService.delete_habits(
        None, 1, 1
    )

    delete_mock.assert_called_once_with(
        None, mock_habit_exists
    )


@pytest.mark.asyncio
async def test_not_update_habit_by_id(mock_no_habit):

    data = object()
    with pytest.raises(HabitNotFoundError):
        await HabitService.update_habits(
            None, 1, 1, data
        )


@pytest.mark.asyncio
async def test_success_update_habit_by_id(monkeypatch, mock_habit_exists):

    habit = mock_habit_exists

    monkeypatch.setattr(
        HabitRepository,
        "get_habits_by_id",
        AsyncMock(return_value=habit)
    )

    data = Mock()
    data.model_dump.return_value = {"name": "new"}

    session = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    result = await HabitService.update_habits(
        session, 1, 1, data
    )

    assert habit.name == "new"

    session.commit.assert_called_once()
    session.refresh.assert_called_once_with(habit)

    assert result == habit


@pytest.mark.asyncio
async def test_create_habit_integrity_error():

    session = AsyncMock()
    data = object()

    session.commit.side_effect = IntegrityError(
        "stmt", "params", Exception()
    )

    data = type("HabitCreate", (), {
        "model_dump": lambda self=None, exclude_unset=True: {
            "name": "test"
        }
    })()

    with pytest.raises(IntegrityError):
        await HabitService.create_habits(
            session, 1, data
        )

    session.rollback.assert_called_once()


@pytest.mark.asyncio
async def test_create_habit_success(monkeypatch):

    data = object()

    create_mock = AsyncMock(return_value={"id": 1})
    monkeypatch.setattr(HabitRepository, "create_habits", create_mock)

    result = await HabitService.create_habits(
        None, 1, data
    )

    assert result == {'id': 1}
