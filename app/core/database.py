from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import DATABASE_URL

# production engine
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)


async def get_session():
    async with SessionLocal() as session:
        yield session


class Base(DeclarativeBase):
    pass


# =========================
# TESTING SUPPORT (IMPORTANT)
# =========================

TestSessionLocal = None
test_engine = None


async def override_get_session():
    """
    Used ONLY in tests via dependency override.
    """
    async with TestSessionLocal() as session:
        yield session