from psycopg import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habits import Habit
from app.schemas.habits import HabitUpdate, HabitCreate
from fastapi import HTTPException, status
from app.repositories.habits import HabitRepository
from app.core.exceptions import HabitNotFoundError

class HabitService:

    @staticmethod
    async def create_habits(
            session: AsyncSession,
            user_id: int,
            data: HabitCreate
    ):
            return await HabitRepository.create_habits(session, user_id, data)


    @staticmethod
    async def get_all_habits(session: AsyncSession, user_id: int):
        return await HabitRepository.get_all_habits(session, user_id)


    @staticmethod
    async def get_habits_by_id(
            session: AsyncSession,
            habit_id: int,
            user_id: int
    ) -> Habit | None:
        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        return habit

    @staticmethod
    async def delete_habits(session: AsyncSession, habit_id: int, user_id: int) -> Habit:
        habit = await HabitRepository.get_habits_by_id(
            session,
            habit_id,
            user_id
        )

        if not habit:
            raise HabitNotFoundError()

        result = await HabitRepository.delete(session, habit)

    @staticmethod
    async def update_habits(session: AsyncSession, habit_id: int, user_id: int, data: HabitUpdate) -> Habit | None:
        result = await session.execute(
            select(Habit).where(
                Habit.id == habit_id,
                Habit.user_id == user_id
            )
        )

        habit = result.scalar_one_or_none()

        if not habit:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(habit, key, value)

        await session.commit()
        await session.refresh(habit)
        return habit
