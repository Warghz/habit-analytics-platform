import pandas as pd
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns


class HabitHeatmap:

    @staticmethod
    def built_df(logs):
        if not logs:
            return pd.DataFrame(columns=['date'])

        return pd.DataFrame([
            {"date": log.completed_date}
            for log in logs
        ])

    @staticmethod
    def generate_heatmap(df: pd.DataFrame):
        if df.empty:
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "No data", ha='center')
            ax.axis('off')
            return fig

        df['date'] = pd.to_datetime(df['date'])

        df['day'] = df['date'].dt.dayofweek
        df['week'] = df['date'].dt.isocalendar().week

        pivot = df.pivot_table(
            index='day',
            columns='week',
            values='date',
            aggfunc='count',
            fill_value=0
        )

        plt.figure(figsize=(12, 4))
        sns.heatmap(
            pivot,
            cmap="Greens",
            linewidths=0.5,
            linecolor="gray"
        )

        plt.title("Habit heatmap")
        plt.ylabel("Day of Week (0=Mon)")
        plt.xlabel("Week Number")

        return plt.gcf()