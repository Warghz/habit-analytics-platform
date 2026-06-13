from starlette.responses import StreamingResponse
from io import BytesIO
from app.analytics.habit_heatmap import HabitHeatmap
from app.repositories.habit_log import HabitLogRepository
from app.repositories.habits import HabitRepository
from app.analytics.habit_analytics import HabitAnalytics
from app.core.exceptions import HabitNotFoundError


class HabitAnalyticsService:

    @staticmethod
    async def get_habit_stats(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)
        if not habit:
            raise HabitNotFoundError()

        logs = await HabitLogRepository.get_logs(session, habit_id)

        df = HabitAnalytics.build_df(logs)

        return {
            "habit_id": habit_id,
            "streak": HabitAnalytics.calculate_streak(df),
            "total_completions": HabitAnalytics.total_comp(df),
            "active_days": HabitAnalytics.active_days(df),
            "completion_rate_30d": HabitAnalytics.completion_rate(df, 30),
        }

    @staticmethod
    async def get_heatmap(session, habit_id: int, user_id: int):

        habit = await HabitRepository.get_habits_by_id(session, habit_id, user_id)

        if not habit:
            raise HabitNotFoundError()

        logs = await HabitLogRepository.get_logs(session, habit_id)

        df = HabitHeatmap.built_df(logs)
        fig = HabitHeatmap.generate_heatmap(df)

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)

        return StreamingResponse(buf, media_type="image/png")