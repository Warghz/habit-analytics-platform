from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import verify_password, create_access_token
from ..database import get_session
from app.schemas.users import UserCreate
from app.models.users import User

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/login")
async def login(
        user_data: UserCreate,
        session: AsyncSession = Depends(get_session)
):
    result = await session.execute(
        select(User).where(User.email == user_data.email)
    )

    user = result.scalar_one_on_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    if not verify_password(user_data.password, User.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    token = create_access_token(
        data={'sub': str(user.id)}
    ) # TO DO

    return {
        "access_token": token,
        "token_type": "bearer"
    }