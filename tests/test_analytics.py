import pandas as pd
import pytest
from app.analytics.habit_analytics import HabitAnalytics
from datetime import date


"""HabitAnalytics.build_df"""

def test_built_df_empty():
    result = HabitAnalytics.build_df([])

    assert isinstance(result, pd.DataFrame)
    assert result.empty
    assert list(result.columns) == ['date']


class FakeLog:
    def __init__(self, completed_date):
        self.completed_date = completed_date


def test_built_df_single_log():
    log = FakeLog(date(2026, 6, 13))

    result = HabitAnalytics.build_df([log])

    assert len(result) == 1
    assert "date" in result.columns
    assert result.iloc[0]['date'] == date(2026, 6, 13)

"""HabitAnalytics - heatmap"""

def test_heatmap_matrix_shape():
    df = pd.DataFrame({
        "date": [date(2026, 6, 13)]
    })

    matrix, df_daily = HabitAnalytics.build_heatmap_matrix(df)

    assert matrix.shape == (7, 52)

def test_heatmap_single_value():
    df = pd.DataFrame({
        "date": [date(2026, 6, 13)]
    })

    matrix, _ = HabitAnalytics.build_heatmap_matrix(df)

    total = matrix.values.sum()

    assert total == 1

def test_heatmap_correct_weekday():
    df = ({
        "date": [date(2026, 6,13)]
    })

    matrix, df_daily = HabitAnalytics.build_heatmap_matrix(df)

    monday_row = matrix.iloc[0].sum() # 0 == Monday

    assert monday_row == 1

def test_heatmap_fills_missing_with_zero():
    df = pd.DataFrame({
        "date": [date(2026, 6, 13)]
    })

    matrix, _ = HabitAnalytics.build_heatmap_matrix(df)

    assert (matrix.isna().sum().sum()) == 0

def test_heatmap_multiple_dates():
    df = pd.DataFrame({
        'date': [
            date(2026, 6, 13),
            date(2026, 6, 13),
            date(2026, 6, 13)
        ]
    })

    matrix, _ = HabitAnalytics.build_heatmap_matrix(df)

    assert matrix.values.sum() == 3