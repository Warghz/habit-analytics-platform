import pytest
from sqlalchemy import select

from app.api.main import app
from app.core.dependencies import get_current_user
from app.models.habits import Habit


@pytest.fixture
def auth_as(user):
    async def fake_user():
        return user

    app.dependency_overrides[get_current_user] = fake_user
    yield user
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_get_habits_route_with_database(client, db_session, auth_as):
    db_session.add_all([
        Habit(user_id=auth_as.id, name="read"),
        Habit(user_id=auth_as.id, name="gym"),
    ])
    await db_session.commit()

    response = await client.get("/habits/")

    assert response.status_code == 200
    names = {habit["name"] for habit in response.json()}
    assert names == {"read", "gym"}


@pytest.mark.asyncio
async def test_create_habit_route_with_database(client, db_session, auth_as):
    response = await client.post(
        "/habits/",
        json={
            "name": "wake early",
            "content": "morning routine",
            "rating": 4,
            "must_have": True,
        }
    )

    assert response.status_code == 201
    assert response.json()["name"] == "wake early"

    result = await db_session.execute(
        select(Habit).where(
            Habit.id == response.json()["id"],
            Habit.user_id == auth_as.id,
        )
    )
    habit = result.scalar_one_or_none()

    assert habit is not None
    assert habit.content == "morning routine"
    assert habit.rating == 4
    assert habit.must_have is True


@pytest.mark.asyncio
async def test_get_habit_by_id_route_with_database(client, db_session, auth_as):
    habit = Habit(user_id=auth_as.id, name="journal")
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    response = await client.get(f"/habits/{habit.id}")

    assert response.status_code == 200
    assert response.json() == {"id": habit.id, "name": "journal"}


@pytest.mark.asyncio
async def test_update_habit_route_with_database(client, db_session, auth_as):
    habit = Habit(user_id=auth_as.id, name="old name")
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    response = await client.put(
        f"/habits/{habit.id}",
        json={"name": "new name"}
    )

    assert response.status_code == 200
    assert response.json() == {"id": habit.id, "name": "new name"}


@pytest.mark.asyncio
async def test_delete_habit_route_with_database(client, db_session, auth_as):
    habit = Habit(user_id=auth_as.id, name="delete me")
    db_session.add(habit)
    await db_session.commit()
    await db_session.refresh(habit)

    response = await client.delete(f"/habits/{habit.id}")

    assert response.status_code == 204

    result = await db_session.execute(select(Habit).where(Habit.id == habit.id))
    assert result.scalar_one_or_none() is None


@pytest.mark.asyncio
async def test_habit_routes_reject_foreign_habit(client, db_session, user, habit):
    async def other_user():
        return type("User", (), {"id": user.id + 1000, "email": "other@test.com"})()

    app.dependency_overrides[get_current_user] = other_user

    response = await client.get(f"/habits/{habit.id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found."
