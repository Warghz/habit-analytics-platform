import pytest
from app.schemas.habits import HabitCreate
from app.repositories.habits import HabitRepository
from app.models.habits import Habit
from app.tests.api.test_routes_habits import FakeHabitService


@pytest.mark.asyncio
async def test_create_habit(db_session, user):

    data = HabitCreate(
        name="Gym",
        content="training",
        rating=5,
        must_have=True
    )

    habit = await HabitRepository.create_habits(
        db_session, user.id, data
    )

    assert habit.id is not None
    assert habit.user_id == user.id
    assert habit.name == "Gym"
    assert habit.content == "training"
    assert habit.rating == 5
    assert habit.must_have is True


@pytest.mark.asyncio
async def test_get_all_habits(db_session, user):

    habit1 = Habit(
        user_id=user.id,
        name="ice shower",
        content="great practice",
        rating=5,
        must_have=True
    )

    habit2 = Habit(
        user_id=user.id,
        name="read",
        content="develops the brain",
        rating=5,
        must_have=True
    )

    db_session.add_all([habit1, habit2])
    await db_session.commit()

    habits = await HabitRepository.get_all_habits(
        db_session, user.id
    )

    assert len(habits) == 2


@pytest.mark.asyncio
async def test_get_habit_by_id(db_session, user):

    habit = Habit(
        user_id=user.id,
        name="read",
        content="develops the brain",
        rating=5,
        must_have=True
    )

    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    result = await HabitRepository.get_habits_by_id(
        db_session, habit.id, user.id
    )

    assert result is not None
    assert result.id == habit.id


@pytest.mark.asyncio
async def test_delete_habit(db_session, user):

    habit = Habit(
        user_id=user.id,
        name="read",
        content="develops the brain",
        rating=5,
        must_have=True
    )

    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    await HabitRepository.delete(db_session, habit)

    result = await HabitRepository.get_habits_by_id(
        db_session, habit.id, user.id
    )

    assert result is None
