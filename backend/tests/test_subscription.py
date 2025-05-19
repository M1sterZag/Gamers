from types import SimpleNamespace
from unittest.mock import AsyncMock, ANY

import pytest
from starlette import status

from app.subscription.dao import SubscriptionDAO, UserSubscriptionDAO


@pytest.mark.anyio
class TestSubscriptionAPI:

    async def test_get_subscriptions(self, client, monkeypatch):
        subs = [
            SimpleNamespace(id=1, name="A", price=100, duration=30),
            SimpleNamespace(id=2, name="B", price=200, duration=60),
        ]
        monkeypatch.setattr(SubscriptionDAO, "find_all", AsyncMock(return_value=subs))

        r = await client.get("/subscriptions")
        assert r.status_code == status.HTTP_200_OK
        body = r.json()
        assert isinstance(body, list) and len(body) == 2
        assert body[0]["id"] == 1 and "price" in body[0]

    async def test_create_subscription(self, client, monkeypatch):
        payload = {"name": "Gold", "price": 999, "duration": 365}
        created = {**payload, "id": 42}
        monkeypatch.setattr(SubscriptionDAO, "add", AsyncMock(return_value=created))

        r = await client.post("/subscriptions", json=payload)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == created
        SubscriptionDAO.add.assert_awaited_once_with(
            session=ANY, **payload
        )

    async def test_delete_subscription_success(self, client, monkeypatch):
        monkeypatch.setattr(SubscriptionDAO, "delete", AsyncMock(return_value=True))

        r = await client.delete("/subscriptions/5")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "Подписка успешно удалена"}
        SubscriptionDAO.delete.assert_awaited_once_with(session=ANY, id=5)

    async def test_delete_subscription_not_found(self, client, monkeypatch):
        monkeypatch.setattr(SubscriptionDAO, "delete", AsyncMock(return_value=False))

        r = await client.delete("/subscriptions/99")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Подписка не найдена"

    async def test_update_subscription_success(self, client, monkeypatch):
        payload = {"name": "Silver", "price": 500, "duration": 180}
        monkeypatch.setattr(SubscriptionDAO, "update", AsyncMock(return_value=1))

        r = await client.put("/subscriptions/7", json=payload)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "success"}
        SubscriptionDAO.update.assert_awaited_once_with(
            filter_by={"id": 7},
            session=ANY,
            **payload
        )

    async def test_update_subscription_not_found(self, client, monkeypatch):
        monkeypatch.setattr(SubscriptionDAO, "update", AsyncMock(return_value=0))
        payload = {"name": "Silver", "price": 500, "duration": 180}

        r = await client.put("/subscriptions/123", json=payload)
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Подписка не найдена"

    async def test_check_subscription_success(self, client, monkeypatch):
        usub = SimpleNamespace(
            id=1, user_id=1, subscription_id=2,
            start_date="2025-01-01", end_date="2025-02-01", is_active=True
        )
        monkeypatch.setattr(UserSubscriptionDAO, "find_active_subscription", AsyncMock(return_value=usub))

        r = await client.get("/subscriptions/check_subscription")
        assert r.status_code == status.HTTP_200_OK
        body = r.json()
        assert body["user_id"] == 1 and body["is_active"] is True

    async def test_check_subscription_not_found(self, client, monkeypatch):
        monkeypatch.setattr(UserSubscriptionDAO, "find_active_subscription", AsyncMock(return_value=None))

        r = await client.get("/subscriptions/check_subscription")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "У вас нет активной подписки"

    async def test_get_subscribed_user_ids(self, client, monkeypatch):
        monkeypatch.setattr(UserSubscriptionDAO, "get_all_subscribed_user_ids", AsyncMock(return_value=[1, 2, 3]))

        r = await client.get("/subscriptions/subscribed_user_ids")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == [1, 2, 3]
