from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.routers import users_router, habits_router, auth_router, admin_router, habit_log_router
from app.tests.test import router as test_router
from app.core.database import engine, get_session
from contextlib import asynccontextmanager
from app.core.exceptions import (
    HabitNotFoundError,
    HabitAlreadyExistsError,
    ForbiddenError,
    AlreadyCompletedTodayError
)
from app.core.exception_handlers import (
    habit_not_found_handler,
    habit_already_exists_handler,
    forbidden_handler,
    already_completed_handler
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(habits_router)
app.include_router(users_router)
app.include_router(auth_router)
app.include_router(test_router)
app.include_router(admin_router)
app.include_router(habit_log_router)

app.add_exception_handler(HabitAlreadyExistsError, habit_already_exists_handler)
app.add_exception_handler(HabitNotFoundError, habit_not_found_handler)
app.add_exception_handler(ForbiddenError, forbidden_handler)
app.add_exception_handler(AlreadyCompletedTodayError, already_completed_handler)

@app.get('/test-db')
async def test_db(
        session: AsyncSession = Depends(get_session)
):
    return {"message": "OK"}


