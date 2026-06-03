from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = DATABASE_URL = "postgresql+asyncpg://postgres:5665@localhost/fastapi"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_session():
    async with SessionLocal() as session:
        yield session