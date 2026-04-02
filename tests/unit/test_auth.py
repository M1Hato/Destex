from app.core.security import hash_password, verify_password


def test_auth_password():
    password = "secret1234"

    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpwd", hashed) is False