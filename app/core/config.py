
import os


def _normalize_database_url(url: str, driver: str) -> str:
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)

    if url.startswith("postgresql://"):
        return url.replace("postgresql://", f"postgresql+{driver}://", 1)

    return url


RAW_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:5665@localhost/fastapi"
)

DATABASE_URL = _normalize_database_url(RAW_DATABASE_URL, "asyncpg")

ALEMBIC_DATABASE_URL = _normalize_database_url(
    os.getenv("ALEMBIC_DATABASE_URL", RAW_DATABASE_URL),
    "asyncpg"
)
