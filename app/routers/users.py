from typing import List
from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.users import UserCreate, UserOut
from app.models.users import User
from app.database import get_session
from app.core.security import hash_password

router = APIRouter(
    prefix="/users",
    tags=['users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(
        user: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )

    find_user = result.scalar_one_or_none()

    if find_user is None:
        raise HTTPException(status_code=404, detail="User not found.")

    return find_user


@router.get("/", response_model=List[UserOut])
async def get_users(session: AsyncSession = Depends(get_session)):

    result = await session.execute(select(User))
    users = result.scalars().all()

    return users


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(select(User).where(User.id == user_id))
    del_user = result.scalar_one_or_none()

    if del_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    await session.delete(del_user)
    await session.commit()
