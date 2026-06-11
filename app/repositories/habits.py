from psycopg import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habits import Habit
from app.schemas.habits import HabitUpdate, HabitCreate, HabitOut
from sqlalchemy import select
from fastapi import HTTPException, status

from app.core.exceptions import HabitNotFoundError


class HabitRepository:

    @staticmethod
    async def create_habits(
            session: AsyncSession,
            user_id: int,
            data: HabitCreate
    ) -> Habit:
        data_dict = data.model_dump(exclude_unset=True)

        habit = Habit(**data_dict, user_id=user_id)

        session.add(habit)
        try:
            await session.commit()
            await session.refresh(habit)
            return habit
        except IntegrityError:
            await session.rollback()
            raise

    @staticmethod
    async def get_all_habits(
            session: AsyncSession,
            user_id: int,
    ):
        result = await session.execute(
            select(Habit).where(Habit.user_id == user_id)
        )
        return result.scalars().all()


    @staticmethod
    async def get_habits_by_id(
            session: AsyncSession,
            habit_id: int,
            user_id: int
    ) -> Habit | None:
        result = await session.execute(
            select(Habit).where(
                Habit.id == habit_id,
                Habit.user_id == user_id
            )
        )
        habit = result.scalar_one_or_none()
        return habit

    @staticmethod
    async def delete(session, habit: Habit):
        await session.delete(habit)
        await session.commit()
        return habit
