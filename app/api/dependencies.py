from app.services.habits import HabitService
from app.services.habit_log import HabitLogService

def get_habit_service():
    return HabitService


def get_habit_log_service():
    return HabitLogService