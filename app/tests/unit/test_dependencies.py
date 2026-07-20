import pytest
from fastapi import HTTPException

from app.core.dependencies import get_current_user, require_admin
from app.core.security import create_access_token
from app.models.users import User


@pytest.mark.asyncio
async def test_get_current_user_success(db_session, user):
    token = create_access_token({"sub": str(user.id)})

    result = await get_current_user(token=token, session=db_session)

    assert result.id == user.id
    assert result.email == user.email


@pytest.mark.asyncio
async def test_get_current_user_rejects_invalid_token(db_session):
    with pytest.raises(HTTPException) as exc:
        await get_current_user(token="not-a-token", session=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "invalid authentication credentials"


@pytest.mark.asyncio
async def test_get_current_user_rejects_token_without_subject(db_session):
    token = create_access_token({"email": "test@test.com"})

    with pytest.raises(HTTPException) as exc:
        await get_current_user(token=token, session=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "invalid authentication credentials"


@pytest.mark.asyncio
async def test_get_current_user_rejects_unknown_user(db_session):
    token = create_access_token({"sub": "999999"})

    with pytest.raises(HTTPException) as exc:
        await get_current_user(token=token, session=db_session)

    assert exc.value.status_code == 401
    assert exc.value.detail == "invalid authentication credentials"


def test_require_admin_success():
    user = User(
        id=1,
        email="admin@test.com",
        hashed_password="fakehash",
        is_admin=True,
    )

    assert require_admin(user) == user


def test_require_admin_rejects_regular_user():
    user = User(
        id=1,
        email="user@test.com",
        hashed_password="fakehash",
        is_admin=False,
    )

    with pytest.raises(HTTPException) as exc:
        require_admin(user)

    assert exc.value.status_code == 403
    assert exc.value.detail == "Admin acess required."
