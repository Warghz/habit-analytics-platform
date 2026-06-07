from datetime import datetime
from sqlalchemy import Integer, String, SMALLINT, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Habit(Base):
    __tablename__ = "habits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(255))
    content: Mapped[str | None] = mapped_column(nullable=True)
    rating: Mapped[int | None] = mapped_column(SMALLINT, nullable=True)
    must_have: Mapped[bool | None] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="habits")

