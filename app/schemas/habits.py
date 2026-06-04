from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitOut(BaseModel):
    id: int
    name: str
    content: Optional[str]
    rating: int
    must_have: bool
    created_at: datetime

class HabitCreate(BaseModel):
    name: str
    content: str
    rating: int
    must_have: bool

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    content: Optional[str] = None
    rating: Optional[int] = None
    must_have: Optional[bool] = None