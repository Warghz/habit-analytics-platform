from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    HabitNotFoundError,
    HabitAlreadyExistsError,
    ForbiddenError,
    AlreadyCompletedTodayError
)


def create_error_response(status_code: int, message: str):
    return JSONResponse(
        status_code=status_code,
        content={"detail": message}
    )
#habits

async def habit_not_found_handler(request: Request, exc: HabitNotFoundError):
    return create_error_response(404, "Habit not found.")


async def habit_already_exists_handler(request: Request, exc: HabitAlreadyExistsError):
    return create_error_response(400, "Habit already exists.")


async def forbidden_handler(request: Request, exc: ForbiddenError):
    create_error_response(403, "Forbidden.")

#habitlog

async def already_completed_handler(request: Request, exc: AlreadyCompletedTodayError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Habit already completed today."}
    )