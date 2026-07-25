from sqlalchemy import select, func
from app.models.habit_logs import HabitLog
from app.models.habits import Habit
from datetime import date


class HabitLogRepository:

    @staticmethod
    async def get_logs(session, habit_id: int, user_id: int):
        stmt = (
            select(HabitLog)
            .join(Habit)
            .where(
                HabitLog.habit_id == habit_id,
                Habit.user_id == user_id
            )
        )
        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def exists_today(session, habit_id: int, user_id: int) -> bool:
        stmt = (
            select(HabitLog.id)
            .join(Habit)
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
        log = HabitLog(
            habit_id=habit_id,
            completed_date=date.today()
        )

        session.add(log)
        await session.commit()
        await session.refresh(log)

        return log

    @staticmethod
    async def get_completion_dates(session, habit_id: int):
        stmt = select(HabitLog.completed_date).where(
            HabitLog.habit_id == habit_id
        )

        result = await session.execute(stmt)

        return list(result.scalars().all())