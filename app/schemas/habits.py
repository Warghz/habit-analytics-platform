from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class HabitOut(BaseModel):
    id: int
    name: str
    content: Optional[str] = None
    rating: int = 0
    must_have: bool = False
    created_at: Optional[datetime] = None


class HabitCreate(BaseModel):
    name: str
    content: Optional[str] = None
    rating: Optional[int] = 0
    must_have: Optional[bool] = False


class HabitUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None
    must_have: Optional[bool] = None