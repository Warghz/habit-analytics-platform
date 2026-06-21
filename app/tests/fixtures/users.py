from uuid import uuid4
import pytest_asyncio
from app.models.users import User

@pytest_asyncio.fixture
async def user(db_session):
    u = User(
        email=f"test-{uuid4().hex}@test.com",
        hashed_password="fakehash"
    )

    db_session.add(u)
    await db_session.commit()
    await db_session.refresh(u)

    return u
