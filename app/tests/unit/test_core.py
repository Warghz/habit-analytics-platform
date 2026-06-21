from app.core.security import hash_password, verify_password, create_access_token

"""SECURITY TESTS"""
def test_hash_password():
    password = "password123"

    hashed_pass= hash_password(password)

    assert hashed_pass != password

def test_verify_password():
    password = 'password123'

    hashed = hash_password(password)

    assert verify_password(password, hashed) is True

def test_verify_wrong_password():
    password = "password123"

    hashed = hash_password(password)

    assert verify_password("wrong", hashed) is False

def test_create_access_token():
    token = create_access_token({"sub": "1"})

    assert isinstance(token, str)
    assert len(token) > 0
