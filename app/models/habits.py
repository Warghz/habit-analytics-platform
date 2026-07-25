from datetime import datetime
from sqlalchemy import String, SMALLINT, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.habit_logs import HabitLog

if TYPE_CHECKING:
    pass


class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(nullable=True)
    rating: Mapped[int | None] = mapped_column(SMALLINT, nullable=True)
    must_have: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="habits")
    logs: Mapped[List["HabitLog"]] = relationship(
        "HabitLog",
        back_populates="habit",
        cascade="all, delete-orphan"
    )