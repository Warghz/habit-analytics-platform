from typing import List
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.users import UserCreate, UserOut
from app.models.users import User
from app.database import get_session
from app.core.security import hash_password
from app.core.security import get_current_user


router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.get('/me', response_model=UserOut)
async def get_me(
        current_user: User = Depends(get_current_user)
):
    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        session: AsyncSession = Depends(get_session),
        current_user: User = Depends(get_current_user)
):
    result = await session.execute(
        select(User).where(User.id == current_user.id)
    )
    user = result.scalar_one_or_none()

    if user:
        await session.delete(current_user)
        await session.commit()
