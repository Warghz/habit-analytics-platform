import pytest
from datetime import date
from app.tests.fixtures.users import user
from app.models.habit_logs import HabitLog
from app.repositories.habit_log import HabitLogRepository


@pytest.mark.asyncio
async def test_create_log(db_session, user, habit):

    log = await HabitLogRepository.create_log(
        db_session, habit.id
    )

    assert log.id is not None
    assert log.habit_id == habit.id


@pytest.mark.asyncio
async def test_not_exists_today(db_session, user, habit):

    result = await HabitLogRepository.exists_today(
        db_session, habit.id, user.id
    )

    assert result is False


@pytest.mark.asyncio
async def test_success_exists_today(db_session, user, habit):

    log = HabitLog(
        habit_id=habit.id,
        completed_date=date.today()
    )

    db_session.add(log)
    await db_session.commit()
    await db_session.refresh(log)

    result = await HabitLogRepository.exists_today(
        db_session, habit.id, user.id
    )

    assert result is True


@pytest.mark.asyncio
async def test_get_logs(db_session, user, habit):

    log_1 = HabitLog(habit_id=habit.id)
    log_2 = HabitLog(habit_id=habit.id)

    db_session.add_all([log_1, log_2])
    await db_session.commit()

    logs = await HabitLogRepository.get_logs(
        db_session, habit.id, user.id
    )

    assert len(logs) == 2


@pytest.mark.asyncio
async def test_get_completion_dates(db_session, user, habit):

    log_1 = HabitLog(
        habit_id=habit.id,
        completed_date=date.today()
    )
    log_2 = HabitLog(
        habit_id=habit.id,
        completed_date=date.today()
    )

    db_session.add_all([log_1, log_2])
    await db_session.commit()

    dates = await HabitLogRepository.get_completion_dates(
        db_session, habit.id
    )

    assert len(dates) == 2