from datetime import date

import pytest

from app.api.main import app
from app.core.dependencies import get_current_user
from app.models.habit_logs import HabitLog


@pytest.fixture
def auth_as(user):
    async def fake_user():
        return user

    app.dependency_overrides[get_current_user] = fake_user
    yield user
    app.dependency_overrides.pop(get_current_user, None)


@pytest.mark.asyncio
async def test_complete_habit_route(client, db_session, auth_as, habit):
    response = await client.post(f"/habit_logs/{habit.id}/complete")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] is not None
    assert body["habit_id"] == habit.id


@pytest.mark.asyncio
async def test_complete_habit_route_already_completed(client, db_session, auth_as, habit):
    db_session.add(HabitLog(habit_id=habit.id, completed_date=date.today()))
    await db_session.commit()

    response = await client.post(f"/habit_logs/{habit.id}/complete")

    assert response.status_code == 400
    assert response.json()["detail"] == "Habit already completed today."


@pytest.mark.asyncio
async def test_complete_habit_route_not_found(client, auth_as):
    response = await client.post("/habit_logs/999999/complete")

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found."


@pytest.mark.asyncio
async def test_get_streak_route(client, db_session, auth_as, habit):
    db_session.add(HabitLog(habit_id=habit.id, completed_date=date.today()))
    await db_session.commit()

    response = await client.get(f"/habit_logs/{habit.id}/streak")

    assert response.status_code == 200
    assert response.json() == {"streak": 1}


@pytest.mark.asyncio
async def test_get_history_route(client, db_session, auth_as, habit):
    db_session.add(HabitLog(habit_id=habit.id, completed_date=date.today()))
    await db_session.commit()

    response = await client.get(f"/habit_logs/{habit.id}/history")

    assert response.status_code == 200
    assert response.json() == {"dates": [date.today().isoformat()]}


@pytest.mark.asyncio
async def test_get_analytics_route(client, db_session, auth_as, habit):
    db_session.add(HabitLog(habit_id=habit.id, completed_date=date.today()))
    await db_session.commit()

    response = await client.get(f"/habit_logs/{habit.id}/analytics")

    assert response.status_code == 200
    body = response.json()
    assert body["habit_name"] == habit.name
    assert body["streak"] == 1
    assert body["total_completions"] == 1
    assert body["active_days"] == 1


@pytest.mark.asyncio
async def test_get_heatmap_route(client, db_session, auth_as, habit):
    db_session.add(HabitLog(habit_id=habit.id, completed_date=date.today()))
    await db_session.commit()

    response = await client.get(f"/habit_logs/{habit.id}/heatmap")

    assert response.status_code == 200
    assert response.headers["content-type"] == "image/png"
    assert response.content.startswith(b"\x89PNG")


@pytest.mark.asyncio
async def test_get_heatmap_route_without_logs_returns_not_found(client, auth_as, habit):
    response = await client.get(f"/habit_logs/{habit.id}/heatmap")

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found."


@pytest.mark.asyncio
async def test_habit_log_routes_reject_foreign_habit(client, db_session, user, habit):
    async def other_user():
        return type("User", (), {"id": user.id + 1000, "email": "other@test.com"})()

    app.dependency_overrides[get_current_user] = other_user

    response = await client.get(f"/habit_logs/{habit.id}/analytics")

    assert response.status_code == 404
    assert response.json()["detail"] == "Habit not found."
