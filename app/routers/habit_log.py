from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from core.dependencies import get_current_user
from app.models.users import User
from services.habit_log import HabitLogService

router = APIRouter(
    prefix='habit_log',
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