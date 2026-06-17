from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.users import User
from app.services.habit_log import HabitLogService
from app.services.habit_analytics import HabitAnalyticsService

router = APIRouter(
    prefix='/habit_logs',
    tags=['habit_log']
)

@router.post('/{habit_id}/complete')
async def complete_habit(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitLogService.complete_habit(session, habit_id, current_user.id)

@router.get("/{habit_id}/streak")
async def get_streak(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return {
        "streak": await HabitLogService.get_streak(session, habit_id, current_user.id)
    }

@router.get("/{habit_id}/history")
async def get_history(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return {
        'dates': await HabitLogService.get_history(
            session,
            habit_id,
            current_user.id
        )
    }

"""analytics """

@router.get("/{habit_id}/analytics")
async def get_analytics(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitAnalyticsService.get_habit_stats(
        session,
        habit_id,
        current_user.id
    )

@router.get('/{habit_id}/heatmap')
async def get_heatmap(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitAnalyticsService.get_heatmap(
        session,
        habit_id,
        current_user.id
    )