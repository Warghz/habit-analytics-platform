from psycopg_pool import AsyncConnectionPool

DATABASE_URL = "postgresql://postgres:5665@localhost:5432/fastapi"

pool = AsyncConnectionPool(
    conninfo=DATABASE_URL,
    min_size=1,
    max_size=10,
    open=False
)


async def open_db():
    await pool.open()


async def close_db():
    await pool.close()


async def get_connection():
    async with pool.connection() as conn:
        yield conn