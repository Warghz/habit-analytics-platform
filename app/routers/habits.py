from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.habits import HabitOut, HabitCreate, HabitUpdate
from app.core.database import get_session
from app.models.users import User
from app.core.dependencies import get_current_user
from app.api.dependencies import get_habit_service

router = APIRouter(
    prefix="/habits",
    tags=["habits"]
)


def short_habit(habit):
    return {
        "id": habit["id"] if isinstance(habit, dict) else habit.id,
        "name": habit["name"] if isinstance(habit, dict) else habit.name
    }


@router.get("/", response_model=list[dict])
async def get_habits(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    service=Depends(get_habit_service)
):
    habits = await service.get_all_habits(session, current_user.id)
    return [short_habit(h) for h in habits]


@router.get("/{habit_id}", response_model=dict)
async def get_habit_by_id(
    habit_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    service=Depends(get_habit_service)
):
    habit = await service.get_habits_by_id(session, habit_id, current_user.id)
    return short_habit(habit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=dict)
async def create_habit(
    habit: HabitCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    service=Depends(get_habit_service)
):
    result = await service.create_habits(session, current_user.id, habit)
    return short_habit(result)


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
    habit_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    service=Depends(get_habit_service)
):
    await service.delete_habits(session, habit_id, current_user.id)
    return None


@router.put("/{habit_id}", response_model=dict)
async def put_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
    service=Depends(get_habit_service)
):
    habit = await service.update_habits(
        session,
        habit_id,
        current_user.id,
        habit_data
    )

    return short_habit(habit)
