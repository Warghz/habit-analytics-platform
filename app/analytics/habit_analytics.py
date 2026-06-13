import pandas as pd
from datetime import date, timedelta

class HabitAnalytics:

    @staticmethod
    def build_df(logs):
        if not logs:
            return pd.DataFrame(columns=['date'])

        return pd.DataFrame([
            {"date": log.completed_date}
            for log in logs
        ])

    @staticmethod
    def calculate_streak(df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        dates = sorted(df['date'].unique(), reverse=True)

        streak = 0
        today = date.today()
        for d in dates:
            if d == today - timedelta(days=streak):
                streak +=1
            else:
                break
        return streak

    @staticmethod
    def total_comp(df: pd.DataFrame) -> int:
        return len(df)

    @staticmethod
    def active_days(df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        return df['date'].nunique()

    @staticmethod
    def completion_rate(df: pd.DataFrame, days: int = 30) -> float:
        today = date.today()
        start = today - timedelta(days=days)

        total_possible_days = days + 1

        if df.empty:
            return 0.0

        actual = df[df['date'] >= start]['date'].nunique()

        return round(actual / total_possible_days, 2)