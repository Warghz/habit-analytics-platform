from uuid import uuid4

import pytest
from sqlalchemy import select

from app.api.main import app
from app.core.dependencies import get_current_user, require_admin
from app.models.habits import Habit
from app.models.users import User


@pytest.fixture
async def admin_user(db_session):
    user = User(
        email=f"admin-{uuid4().hex}@test.com",
        hashed_password="fakehash",
        is_admin=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.fixture
def auth_as_admin(admin_user):
    async def fake_admin():
        return admin_user

    app.dependency_overrides[get_current_user] = fake_admin
    app.dependency_overrides[require_admin] = fake_admin
    yield admin_user
    app.dependency_overrides.pop(get_current_user, None)
    app.dependency_overrides.pop(require_admin, None)


@pytest.mark.asyncio
async def test_admin_get_users_route(client, auth_as_admin):
    response = await client.get("/admin/users")

    assert response.status_code == 200
    assert any(user["id"] == auth_as_admin.id for user in response.json())


@pytest.mark.asyncio
async def test_admin_get_habits_route(client, db_session, auth_as_admin):
    habit = Habit(user_id=auth_as_admin.id, name="admin habit")
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    response = await client.get("/admin/habits")

    assert response.status_code == 200
    assert any(item["id"] == habit.id for item in response.json())


@pytest.mark.asyncio
async def test_admin_delete_user_route(client, db_session, auth_as_admin):
    user = User(
        email=f"delete-{uuid4().hex}@test.com",
        hashed_password="fakehash",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    response = await client.delete(f"/admin/users/{user.id}")

    assert response.status_code == 204

    result = await db_session.execute(select(User).where(User.id == user.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_admin_delete_unknown_user_route(client, auth_as_admin):
    response = await client.delete("/admin/users/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found."


@pytest.mark.asyncio
async def test_admin_routes_forbid_non_admin(client, user):
    async def fake_user():
        return user

    app.dependency_overrides[get_current_user] = fake_user

    response = await client.get("/admin/users")

    assert response.status_code == 403
    assert response.json()["detail"] == "Admin acess required."
