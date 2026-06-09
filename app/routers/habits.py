from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.habits import Habit
from app.schemas.habits import HabitOut, HabitCreate, HabitUpdate
from ..database import get_session
from app.core.security import get_current_user
from app.models.users import User
from core.dependencies import get_current_user

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

    result = await session.execute(
        select(Habit).Where(Habit.user_id == current_user.id)
    )
    habits = result.scalars().all()

    return habits


@router.get('/{habit_id}', response_model=HabitOut)
async def get_habit_by_id(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        )
    )
    habit = result.scalar_one_or_none()

    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found.")

    return habit


@router.post("/", response_model=HabitOut, status_code=status.HTTP_201_CREATED)
async def create_habit(
        habit: HabitCreate,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    db_habit = Habit(**habit.model_dump(), user_id=current_user.id)
    session.add(db_habit)
    await session.commit()
    await session.refresh(db_habit)
    return db_habit


@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_habit(
        habit_id: int,
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(Habit).where(
            Habit.id == habit_id,
            Habit.user_id == current_user.id
        )
    )

    habit = result.scalar_one_or_none()

    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    await session.delete(habit)
    await session.commit()


@router.put("/{habit_id}", response_model=HabitOut)
async def put_habit(
        habit_id: int,
        habit_data: HabitUpdate,
        session: AsyncSession = Depends(get_session)
):
        result = await session.execute(
            select(Habit).where(Habit.id == habit_id)
        )
        habit = result.scalar_one_or_none()

        if habit is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f'Error: habit not found'
            )

        for key, value in habit_data.model_dump(exclude_unset=True).items():
            setattr(habit, key, value)

        await session.commit()
        await session.refresh(habit)

        return habit
