import pytest
from sqlalchemy import select

from app.core.security import hash_password
from app.models.users import User


async def create_user(db_session, email: str, password: str = "secret123"):
    user = User(
        email=email,
        hashed_password=hash_password(password)
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


@pytest.mark.asyncio
async def test_success_auth_register(client, db_session):

    payload = {
        "email": "newuser@test.com",
        "password": "secret123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "User created"
    assert "user_id" in body

    result = await db_session.execute(
        select(User).where(User.email == payload["email"])
    )
    user = result.scalar_one_or_none()

    assert user is not None
    assert user.id == body["user_id"]
    assert user.email == payload["email"]
    assert user.hashed_password != payload['password']


@pytest.mark.asyncio
async def test_not_auth_register(client, db_session):

    await create_user(db_session, "testemail@test.com")

    payload ={
        "email": "testemail@test.com",
        "password": "secret123"
    }

    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


@pytest.mark.asyncio
async def test_register_invalid_email(client):
    response = await client.post(
        "/auth/register",
        json={"email": "not-email", "password": "secret123"}
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_success_auth_login(client, db_session):
    await create_user(db_session, "login@test.com", "secret123")

    payload = {
        "username": "login@test.com",
        "password": "secret123"
    }

    response = await client.post("/auth/login", data=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["token_type"] == "bearer"
    assert isinstance(body["access_token"], str)
    assert body["access_token"]


@pytest.mark.asyncio
async def test_not_auth_login_wrong_password(client, db_session):
    await create_user(db_session, "wrongpass@test.com", "secret123")

    payload = {
        "username": "wrongpass@test.com",
        "password": "wrong-password"
    }

    response = await client.post("/auth/login", data=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"


@pytest.mark.asyncio
async def test_not_auth_login_unknown_user(client):
    payload = {
        "username": "unknown@test.com",
        "password": "secret123"
    }

    response = await client.post("/auth/login", data=payload)

    assert response.status_code == 401
    assert response.json()["detail"] == "invalid credentials"


