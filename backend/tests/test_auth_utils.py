import pytest
from app.auth.utils import get_password_hash, verify_password


@pytest.mark.parametrize("password", [
    "password123",
    "another$ecret!",
    "парольНаРусском",
])
def test_hash_and_verify_roundtrip(password):
    hashed = get_password_hash(password)
    assert isinstance(hashed, str) and len(hashed) > 0

    assert verify_password(password, hashed) is True

    assert verify_password(password + "wrong", hashed) is False


def test_hash_is_salted():
    pwd = "same_password"
    hash1 = get_password_hash(pwd)
    hash2 = get_password_hash(pwd)

    assert hash1 != hash2, "Ожидается, что хеши одного пароля с солью будут различны"
    assert verify_password(pwd, hash1) is True
    assert verify_password(pwd, hash2) is True
