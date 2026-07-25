import pytest
import pytest_asyncio
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.database import Base
from app.core.config import DATABASE_URL
from httpx import AsyncClient, ASGITransport
from app.api.main import app
from app.core.database import get_session
from app.core.dependencies import get_current_user
from app.models.users import User

pytest_plugins = [
    "app.tests.fixtures.users",
    "app.tests.fixtures.habits",
]

# ========================
# TEST DB
# ========================

TEST_DATABASE_URL = DATABASE_URL.replace("fastapi", "habits_test")

engine_test = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

TestingSessionLocal = async_sessionmaker(
    bind=engine_test,
    expire_on_commit=False,
)

# ========================
# DB SETUP / TEARDOWN
# ========================
@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine_test.dispose()


# ========================
# DB SESSION FIXTURE
# ========================
@pytest_asyncio.fixture
async def db_session():
    async with TestingSessionLocal() as session:
        yield session


# ========================
# OVERRIDE DB DEPENDENCY
# ========================
@pytest_asyncio.fixture(autouse=True)
async def override_get_session(db_session):

    async def _override():
        yield db_session

    app.dependency_overrides[get_session] = _override

    yield

    app.dependency_overrides.clear()


# ========================
# DISABLE AUTH (ВАЖНО!)
# ========================
@pytest.fixture(autouse=True)
def disable_auth():

    async def fake_user():
        return User(
            id=1,
            email="test@test.com",
            hashed_password="fake"
        )

    app.dependency_overrides[get_current_user] = fake_user

    yield

    app.dependency_overrides.pop(get_current_user, None)


# ========================
# HTTP CLIENT
# ========================
@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as ac:
        yield ac
