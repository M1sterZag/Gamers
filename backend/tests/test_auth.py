import pytest
from unittest.mock import AsyncMock
import app.auth.utils
from app.auth.dao import UsersDAO
from app.auth.utils import get_password_hash


@pytest.mark.anyio
async def test_register_success(monkeypatch, client):
    monkeypatch.setattr(UsersDAO, "find_one_or_none", AsyncMock(return_value=None))
    monkeypatch.setattr(UsersDAO, "add", AsyncMock(return_value=None))

    response = await client.post("/auth/register", json={
        "email": "test@example.com",
        "username": "testuser",
        "password": "securepass123",
        "confirm_password": "securepass123"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Вы успешно зарегистрированы!"


@pytest.mark.anyio
async def test_register_user_already_exists(monkeypatch, client):
    monkeypatch.setattr(UsersDAO, "find_one_or_none", AsyncMock(return_value=True))

    response = await client.post("/auth/register", json={
        "email": "existing@example.com",
        "username": "existuser",
        "password": "pass123456",
        "confirm_password": "pass123456"
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Пользователь уже существует"


@pytest.mark.anyio
async def test_login_success(monkeypatch, fake_user, client):
    fake_user.password = get_password_hash("securepass123")

    monkeypatch.setattr(
        UsersDAO,
        "find_one_or_none",
        AsyncMock(return_value=fake_user)
    )

    monkeypatch.setattr(app.auth.utils, "set_tokens", lambda r, uid: None)

    response = await client.post("/auth/login", json={
        "email": fake_user.email,
        "password": "securepass123"
    })

    assert response.status_code == 200
    assert response.json()["message"] == "Авторизация успешна!"


@pytest.mark.anyio
async def test_login_incorrect_credentials(monkeypatch, client):
    monkeypatch.setattr(
        UsersDAO,
        "find_one_or_none",
        AsyncMock(return_value=None)
    )

    response = await client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "badpass123"
    })

    assert response.status_code == 400
    assert response.json()["detail"] == 'Неверная почта или пароль'
