import pandas as pd
from datetime import date, timedelta

class HabitAnalytics:

    @staticmethod
    def build_df(logs):
        if not logs:
            return pd.DataFrame(columns=['date'])

        df = pd.DataFrame([
            {"date": log.completed_date}
            for log in logs
        ])

        df['date'] = pd.to_datetime(df['date'])
        return df

    @staticmethod
    def calculate_streak(df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        dates = sorted(df['date'].dt.date.unique(), reverse=True)

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
        today = pd.Timestamp.today().normalize()
        start = today - timedelta(days=days)

        total_possible_days = days + 1

        if df.empty:
            return 0.0

        actual = df[df['date'] >= start]['date'].nunique()

        return round(actual / total_possible_days * 100, 2)

    @staticmethod
    def longest_streak(df: pd.DataFrame) -> int:
        if df.empty:
            return 0

        dates = sorted(df['date'].dt.date.unique())

        longest = 1
        current = 1

        for i in range(1, len(dates)):
            if dates[i] == dates[i-1] + timedelta(days=1):
                current += 1
                longest = max(current, longest)
            else:
                current = 1

        return longest

    @staticmethod
    def best_weekday(df: pd.DataFrame) -> str:
        if df.empty:
            return "No data"

        weekday = (
            df['date']
            .dt.day_name()
            .value_counts()
            .idxmax()
        )

        return weekday

    @staticmethod # use in create graphics with seaborn, matplotlib
    def activity_by_weekday(df: pd.DataFrame) -> dict:
        if df.empty:
            return {}

        return (
            df["date"]
            .dt.day_name()
            .value_counts()
            .to_dict()
        )

    @staticmethod
    def build_heatmap_matrix(df: pd.DataFrame):
        if df.empty:
            return None, None

        data = df.copy()
        data["date"] = pd.to_datetime(data["date"]).dt.normalize()

        # 🔥 фикс: берем ровно 1 год назад от today
        end = pd.Timestamp.today().normalize()
        start = end - pd.Timedelta(days=52 * 7 - 1)

        full_range = pd.date_range(start=start, end=end, freq="D")

        daily = (
            data.groupby("date")
            .size()
            .reindex(full_range, fill_value=0)
        )

        df_daily = pd.DataFrame({
            "date": full_range,
            "count": daily.values
        })

        df_daily["day"] = df_daily["date"].dt.weekday
        df_daily["week"] = (df_daily.index // 7)

        matrix = df_daily.pivot_table(
            index="day",
            columns="week",
            values="count",
            fill_value=0
        )

        matrix = matrix.reindex(index=range(7), columns=range(52), fill_value=0)

        return matrix, df_daily