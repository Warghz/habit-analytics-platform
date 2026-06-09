from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import users_router, habits_router, auth_router
from .database import engine, get_session
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(habits_router)
app.include_router(users_router)
app.include_router(auth_router)

@app.get('/test-db')
async def test_db(
        session: AsyncSession = Depends(get_session)
):
    return {"message": "OK"}


