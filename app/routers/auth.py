from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import verify_password, create_access_token
from app.core.security import hash_password
from app.schemas.auth import UserRegister
from app.core.database import get_session
from app.models.users import User
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
        data: UserRegister,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    new_user = User(
        email=data.email,
        hashed_password=hash_password(data.password)
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }


@router.post("/login")
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == form_data.username)
    )

    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )

    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid credentials"
        )

    token = create_access_token(
        data={"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }