from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, DateTime, func, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.habits import Habit


class HabitLog(Base):
    __tablename__ = "habit_logs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    habit_id: Mapped[int] = mapped_column(
        ForeignKey("habits.id", ondelete="CASCADE")
    )

    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    completed_date: Mapped[date] = mapped_column(
        Date,
        server_default=func.current_date()
    )

    habit = relationship(
        "Habit",
        back_populates="logs"
    )