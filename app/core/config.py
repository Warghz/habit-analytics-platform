
import os


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:5665@localhost/fastapi"
)

ALEMBIC_DATABASE_URL = os.getenv(
    "ALEMBIC_DATABASE_URL",
    "postgresql+psycopg://postgres:5665@localhost/fastapi"
)
