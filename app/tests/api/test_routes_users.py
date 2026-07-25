import pytest
from sqlalchemy import select

from app.api.main import app
from app.core.dependencies import get_current_user
from app.models.users import User


@pytest.fixture
def auth_as(user):
    async def fake_user():
        return user

    app.dependency_overrides[get_current_user] = fake_user
    yield user
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_get_me_route(client, auth_as):
    response = await client.get("/users/me")

    assert response.status_code == 200
    assert response.json()["id"] == auth_as.id
    assert response.json()["email"] == auth_as.email


@pytest.mark.asyncio
async def test_delete_me_route(client, db_session, auth_as):
    response = await client.delete("/users/me")

    assert response.status_code == 204

    result = await db_session.execute(select(User).where(User.id == auth_as.id))
    assert result.scalar_one_or_none() is None
