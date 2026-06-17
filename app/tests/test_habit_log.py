import pytest
from app.core.exceptions import HabitNotFoundError, AlreadyCompletedTodayError
from app.services.habit_log import HabitLogService
from app.repositories.habits import HabitRepository
from unittest.mock import AsyncMock
from app.repositories.habit_log import HabitLogRepository
from datetime import date, timedelta


@pytest.mark.asyncio
async def test_complete_habit_not_found(mock_no_habit):
    with pytest.raises(HabitNotFoundError):
        await HabitLogService.complete_habit(
            session=None,
            habit_id=1,
            user_id=1
        )

@pytest.mark.asyncio
async def test_complete_habit_already_done(
        mock_habit_exists,
        mock_already_done
):
    with pytest.raises(AlreadyCompletedTodayError):
        await HabitLogService.complete_habit(
            session=None,
            habit_id=1,
            user_id=1
        )


@pytest.mark.asyncio
async def test_complete_habit_success(
        mock_habit_exists,
        mock_already_not_done,
        mock_create_log
):
    result = await HabitLogService.complete_habit(
        session=None,
        habit_id=1,
        user_id=1
    )

    assert result == {"log_id": 10}
    HabitLogRepository.create_log.assert_called_once_with(
        None, 1
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "dates, expected",
    [
        # zero days
        ([], 0),

        #one day
        ([date.today()], 1),

        #streak 3 days
        (
            [
                date.today(),
                date.today() - timedelta(days=1),
                date.today() - timedelta(days=2)
            ],
            3
        ),

        #break streak
        (
            [
                date.today(),
                date.today() - timedelta(days=2)
            ],
            1
        )
    ]
)
async def test_get_streak(
        mock_habit_exists,
        dates,
        expected
):
    HabitLogRepository.get_completion_dates = AsyncMock(
        return_value=dates
    )

    result = await HabitLogService.get_streak(
        None, 1, 1
    )

    assert result == expected

