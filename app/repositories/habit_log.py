from sqlalchemy import select, func
from app.models.habit_logs import HabitLog
from app.models.habits import Habit
from datetime import date


class HabitLogRepository:

    @staticmethod
    async def exists_today(session, habit_id: int, user_id: int) -> bool:
        stmt = (
            select(HabitLog.id)
            .join(HabitLog.habit)
            .where(
                HabitLog.habit_id == habit_id,
                Habit.user_id == user_id,
                HabitLog.completed_date == func.current_date()
            )
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none() is not None

    @staticmethod
    async def create_log(session, habit_id: int) -> HabitLog:
        log = HabitLog(habit_id=habit_id)

        session.add(log)
        await session.commit()
        await session.refresh(log)

        return log

    @staticmethod
    async def get_completion_dates(session, habit_id: int) -> list[date]:
        stmt = select(HabitLog.completed_at).where(
            HabitLog.habit_id == habit_id
        )

        result = await session.execute(stmt)
        return [row[0].date() for row in result.all()]

    @staticmethod
    async def get_completion_dates(session, habit_id: int) -> list[date]:

        stmt = select(HabitLog.completed_date).where(HabitLog.habit_id == habit_id)

        result = await session.execute(stmt)

        return result.scalars().all()