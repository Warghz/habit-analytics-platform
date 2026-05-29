from fastapi import FastAPI
from app.routers import habits_router
from .database import open_db, close_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    print("Starting up...")
    await open_db()
    yield
    print("Shutting down...")
    await close_db()

app = FastAPI(lifespan=lifespan)

app.include_router(habits_router)

@app.get('/')
def root():
    return {"message": "OK"}


