import pytest
from httpx import AsyncClient
import httpx
from unittest.mock import AsyncMock
from app.api.main import app
from app.services.habits import HabitService
from app.api.dependencies import get_habit_service


@pytest.fixture
def override_service():
    app.dependency_overrides[get_habit_service] = lambda: FakeHabitService()
    yield
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    transport = httpx.ASGITransport(app=app)

    return httpx.AsyncClient(
        transport=transport,
        base_url="http://test"
    )


class FakeHabitService:
    async def get_all_habits(self, session, user_id):
        return [
            {"id": 1, "name": "ice shower"},
            {"id": 2, "name": "gym"}
        ]

    async def get_habits_by_id(self, session, habit_id, user_id):
        return {"id": habit_id, "name": "ice shower"}

    async def create_habits(self, session, user_id, habit):
        return {"id": 10, "name": "wake early"}

    async def delete_habits(self, session, habit_id, user_id):
        return None

    async def update_habits(self, session, habit_id, user_id):
        return {"id": habit_id, "name": "cardio training"}


@pytest.mark.asyncio
async def test_get_habits_route(client, override_service):

    response = await client.get("/habits")

    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "ice shower"},
        {"id": 2, "name": "gym"},
    ]


@pytest.mark.asyncio
async def test_get_habit_by_id(client, override_service):

    response = await client.get("/habits/1")

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "ice shower"}


@pytest.mark.asyncio
async def test_create_habit(client, override_service):

    response = await client.post(
        "/habits/",
        json={"name": "wake early"}
    )

    assert response.status_code == 201
    assert response.json() == {"id": 10, "name": "wake early"}


@pytest.mark.asyncio
async def test_delete_habit(client, override_service):

    response = await client.delete("/habits/1")

    assert response.status_code == 204


@pytest.mark.asyncio
async def test_update_habit(client, override_service):

    response = await client.put(
        "/habits/1",
        json={"name": "cardio training"}
    )

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "cardio training"}