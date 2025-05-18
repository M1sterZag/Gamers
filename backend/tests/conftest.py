import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock

from app.auth.dependencies import get_current_user, get_current_admin_user
from app.main import app
from app.dao import dependencies


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


def pytest_configure(config):
    config.option.asyncio_default_fixture_loop_scope = "function"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def fake_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def fake_user():
    from app.auth.models import User
    from app.auth.utils import get_password_hash

    return User(
        id=1,
        email="test@example.com",
        username="testuser",
        password=get_password_hash("securepass123"),
        is_active=True,
        is_admin=True
    )


@pytest.fixture(autouse=True)
def override_dependencies(fake_session):
    # Подменяем зависимости на фикстуры с моками
    app.dependency_overrides[dependencies.get_session_with_commit] = lambda: fake_session
    app.dependency_overrides[dependencies.get_session_without_commit] = lambda: fake_session

    app.dependency_overrides[get_current_user] = lambda: fake_user
    app.dependency_overrides[get_current_admin_user] = lambda: fake_user
    yield
    app.dependency_overrides.clear()
