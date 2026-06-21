from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.habits import HabitRepository
from app.schemas.habits import HabitCreate, HabitUpdate
from app.core.exceptions import HabitNotFoundError


class HabitService:

    @staticmethod
    async def create_habits(session, user_id: int, data: HabitCreate):
        return await HabitRepository.create_habits(session, user_id, data)

    @staticmethod
    async def get_all_habits(session, user_id: int):
        return await HabitRepository.get_all_habits(session, user_id)

    @staticmethod
    async def get_habits_by_id(session, habit_id: int, user_id: int):
        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        return habit

    @staticmethod
    async def delete_habits(session, habit_id: int, user_id: int):
        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        await HabitRepository.delete(session, habit)
        return None

    @staticmethod
    async def update_habits(session, habit_id: int, user_id: int, data: HabitUpdate):
        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(habit, key, value)

        await session.commit()
        await session.refresh(habit)
        return habit