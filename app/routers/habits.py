from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habits import Habit
from app.schemas.habits import HabitOut, HabitCreate, HabitUpdate
from ..database import get_session
from app.models.users import User
from app.core.dependencies import get_current_user
from app.services.habits import HabitService

router = APIRouter(
    prefix="/habits",
    tags=['habits']
    # dependencies=[Depends(get_current_user)]
)

@router.get('/', response_model=list[HabitOut])
async def get_habits(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitService.get_all_habits(session, current_user.id)


@router.get('/{habit_id}', response_model=HabitOut)
async def get_habit_by_id(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitService.get_habits_by_id(session, habit_id, current_user.id)


@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
        habit: HabitCreate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    return await HabitService.create_habits(session, current_user.id, habit)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    habit = await HabitService.delete_habits(session, habit_id, current_user.id)

    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found.')




@router.put("/{habit_id}", response_model=HabitOut)
async def put_habit(
        habit_id: int,
        habit_data: HabitUpdate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    habit = await HabitService.update_habits(session, habit_id, current_user.id, habit_data)

    if habit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Habit not found.')

    return habit
