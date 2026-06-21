from datetime import date, timedelta
from app.repositories.habit_log import HabitLogRepository
from app.repositories.habits import HabitRepository
from app.core.exceptions import HabitNotFoundError, AlreadyCompletedTodayError


class HabitLogService:

    @staticmethod
    async def complete_habit(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)
        if not habit:
            raise HabitNotFoundError()

        already_done = await HabitLogRepository.exists_today(session, habit_id, user_id)
        if already_done:
            raise AlreadyCompletedTodayError()

        log = await HabitLogRepository.create_log(session, habit_id)

        return log

    @staticmethod
    async def get_streak(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)
        if not habit:
            raise HabitNotFoundError()

        dates = await HabitLogRepository.get_completion_dates(session, habit_id)

        if not dates:
            return 0

        dates = sorted(set(dates), reverse=True)

        streak = 0
        today = date.today()

        for d in dates:
            if d == today - timedelta(days=streak):
                streak += 1
            else:
                break

        return streak

    @staticmethod
    async def get_history(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)
        if not habit:
            raise HabitNotFoundError()

        return await HabitLogRepository.get_completion_dates(session, habit_id)