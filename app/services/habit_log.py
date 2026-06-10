from app.repositories.habit_log import HabitLogRepository
from app.core.exceptions import AlreadyCompletedTodayError
from app.repositories.habits import HabitRepository # только для get_habits_by_id чтобы проверить на habit_id, user_id !!!
from app.core.exceptions import HabitNotFoundError
from datetime import date, timedelta

class HabitLogService:

    @staticmethod
    async def complete_habit(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        already_done = HabitLogRepository.exists_today(session, habit_id, user_id)

        if already_done:
            raise AlreadyCompletedTodayError()

        return await HabitLogRepository.create_log(session, habit_id)


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
                streak +=1
            else:
                break

            return streak