from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habits import Habit
from app.schemas.habits import HabitUpdate, HabitCreate



class HabitService:

    @staticmethod
    async def create_habits(
            session: AsyncSession,
            user_id: int,
            data: HabitCreate
    ):
        data_dict = data.model_dump(exclude_unset=True)

        habit = Habit(
            **data_dict,
            user_id=user_id
        )
        session.add(habit)
        await session.commit()
        await session.refresh(habit)


    @staticmethod
    async def get_all_habits(session: AsyncSession, user_id: int):
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
        return result.scalar_one_or_none()

    @staticmethod
    async def delete_habits(session: AsyncSession, habit_id: int, user_id: int) -> Habit | None:
        result = await session.execute(
            select(Habit).where(
                Habit.id == habit_id,
                Habit.user_id == user_id
            )
        )

        habit = result.scalar_one_or_none()

        if not habit:
            return None

        await session.delete(habit)
        await session.commit()

        return habit

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
