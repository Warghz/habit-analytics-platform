from sqlalchemy import select
from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import User
from app.models.habits import Habit
from app.core.dependencies import require_admin
from app.database import get_session

router = APIRouter(
    prefix='/admin',
    tags=['admin']
)

@router.get('/users')
async def get_all_users(
        session: AsyncSession = Depends(get_session()),
        admin: User = Depends(require_admin)
):
    result = await session.execute(select(User))

    return result.scalars().all()

@router.get('/habits')
async def get_all_habits(
        session: AsyncSession = Depends(get_session),
        admin: User = Depends(require_admin)
):
    result = await session.execute(select(Habit))
    return result.scalars().all()

@router.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_session),
        admin: User = Depends(require_admin)
):
    stmt = select(User).where(User.id == user_id)

    result = await session.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    await session.delete(user)
    await session.commit()