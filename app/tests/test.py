import asyncpg
import asyncio
from app.models.users import User
from app.core.dependencies import get_current_user
from fastapi import APIRouter, Depends
from app.schemas.users import UserOut

router = APIRouter(
    tags=['test']
)


async def test():
    conn = await asyncpg.connect(
        user="postgres",
        password="YOUR_PASSWORD",
        database="habits",
        host="127.0.0.1",
        port=5432
    )
    print("CONNECTED OK")
    await conn.close()


@router.get('/me', response_model=UserOut)
async def me(
        current_user: User = Depends(get_current_user)
):
    return current_user