from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

DATABASE_URL = ("postgresql+psycopg_async://postrgres:5665@localhost/habits")

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

async def get_session():
    async with SessionLocal() as session:
        yield session