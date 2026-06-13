from starlette.responses import StreamingResponse
from io import BytesIO

from app.analytics.vizualization import HabitVisualization
from app.repositories.habit_log import HabitLogRepository
from app.repositories.habits import HabitRepository
from app.analytics.habit_analytics import HabitAnalytics
from app.core.exceptions import HabitNotFoundError
from fastapi.responses import StreamingResponse


class HabitAnalyticsService:

    @staticmethod
    async def get_habit_stats(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        logs = await HabitLogRepository.get_logs(session, habit_id)

        df = HabitAnalytics.build_df(logs)

        return {
            "habit_name": habit.name,
            "streak": HabitAnalytics.calculate_streak(df),
            "longest_streak": HabitAnalytics.longest_streak(df),
            "total_completions": HabitAnalytics.total_comp(df),
            "best_weekday": HabitAnalytics.best_weekday(df),
            "active_days": HabitAnalytics.active_days(df),
            "completion_rate_30d": HabitAnalytics.completion_rate(df, 30),
        }

    @staticmethod
    async def get_heatmap(session, habit_id: int, user_id: int):

        logs = await HabitLogRepository.get_logs(
            session=session,
            habit_id=habit_id,
            user_id=user_id
        )

        if not logs:
            raise HabitNotFoundError()

        df = HabitAnalytics.build_df(logs)

        if df.empty:
            raise HabitNotFoundError()

        matrix, _ = HabitAnalytics.build_heatmap_matrix(df)

        if matrix is None or matrix.empty:
            raise HabitNotFoundError()

        image = HabitVisualization.create_heatmap(matrix)

        return StreamingResponse(
            image,
            media_type="image/png"
        )