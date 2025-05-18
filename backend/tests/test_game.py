import pytest
from unittest.mock import AsyncMock
from fastapi import status

from app.game.dao import GameDAO, GameTypeDAO

GAME_DATA = {"name": "Test Game", "avatar": "http://example.com/game.jpg"}
UPDATED_GAME_DATA = {"name": "Updated Game", "avatar": "http://example.com/updated.jpg"}

GAME_TYPE_DATA = {"name": "Test Game Type"}
UPDATED_GAME_TYPE_DATA = {"name": "Updated Game Type"}


@pytest.mark.anyio
class TestGamesAPI:
    async def test_create_game_success(self, client, monkeypatch):
        mock_add = AsyncMock(return_value={"id": 1, **GAME_DATA})
        monkeypatch.setattr(GameDAO, "add", mock_add)

        r = await client.post("/games", json=GAME_DATA)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"id": 1, **GAME_DATA}
        mock_add.assert_awaited_once()

    async def test_get_games_success(self, client, monkeypatch):
        mock_list = [{"id": 1, **GAME_DATA}, {"id": 2, **GAME_DATA}]
        mock_find = AsyncMock(return_value=mock_list)
        monkeypatch.setattr(GameDAO, "find_all", mock_find)

        r = await client.get("/games")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == mock_list
        mock_find.assert_awaited_once()

    async def test_update_game_success(self, client, monkeypatch):
        mock_update = AsyncMock(return_value=1)
        monkeypatch.setattr(GameDAO, "update", mock_update)

        r = await client.put("/games/1", json=UPDATED_GAME_DATA)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "success"}
        called_kwargs = mock_update.await_args.kwargs
        assert called_kwargs["filter_by"] == {"id": 1}
        for key, value in UPDATED_GAME_DATA.items():
            assert called_kwargs.get(key) == value

    async def test_update_game_not_found(self, client, monkeypatch):
        monkeypatch.setattr(GameDAO, "update", AsyncMock(return_value=0))

        r = await client.put("/games/999", json=UPDATED_GAME_DATA)
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Игра не найдена"

    async def test_delete_game_success(self, client, monkeypatch):
        mock_delete = AsyncMock(return_value=True)
        monkeypatch.setattr(GameDAO, "delete", mock_delete)

        r = await client.delete("/games/1")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "Игра успешно удалена"}
        mock_delete.assert_awaited_once()
        # Проверяем только id, session пропускаем
        assert mock_delete.await_args.kwargs.get("id") == 1

    async def test_delete_game_not_found(self, client, monkeypatch):
        monkeypatch.setattr(GameDAO, "delete", AsyncMock(return_value=False))

        r = await client.delete("/games/999")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Игра не найдена"


@pytest.mark.anyio
class TestGameTypesAPI:
    async def test_create_game_type_success(self, client, monkeypatch):
        mock_add = AsyncMock(return_value={"id": 1, **GAME_TYPE_DATA})
        monkeypatch.setattr(GameTypeDAO, "add", mock_add)

        r = await client.post("/games/types", json=GAME_TYPE_DATA)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"id": 1, **GAME_TYPE_DATA}
        mock_add.assert_awaited_once()

    async def test_get_game_types_success(self, client, monkeypatch):
        mock_list = [{"id": 1, **GAME_TYPE_DATA}, {"id": 2, **GAME_TYPE_DATA}]
        mock_find = AsyncMock(return_value=mock_list)
        monkeypatch.setattr(GameTypeDAO, "find_all", mock_find)

        r = await client.get("/games/types")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == mock_list
        mock_find.assert_awaited_once()

    async def test_update_game_type_success(self, client, monkeypatch):
        mock_update = AsyncMock(return_value=1)
        monkeypatch.setattr(GameTypeDAO, "update", mock_update)

        r = await client.put("/games/types/1", json=UPDATED_GAME_TYPE_DATA)
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "success"}
        called_kwargs = mock_update.await_args.kwargs
        assert called_kwargs["filter_by"] == {"id": 1}
        for key, value in UPDATED_GAME_TYPE_DATA.items():
            assert called_kwargs.get(key) == value

    async def test_update_game_type_not_found(self, client, monkeypatch):
        monkeypatch.setattr(GameTypeDAO, "update", AsyncMock(return_value=0))

        r = await client.put("/games/types/999", json=UPDATED_GAME_TYPE_DATA)
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Тип игры не найден"

    async def test_delete_game_type_success(self, client, monkeypatch):
        mock_delete = AsyncMock(return_value=True)
        monkeypatch.setattr(GameTypeDAO, "delete", mock_delete)

        r = await client.delete("/games/types/1")
        assert r.status_code == status.HTTP_200_OK
        assert r.json() == {"message": "Тип игры успешно удален"}
        mock_delete.assert_awaited_once()
        assert mock_delete.await_args.kwargs.get("id") == 1

    async def test_delete_game_type_not_found(self, client, monkeypatch):
        monkeypatch.setattr(GameTypeDAO, "delete", AsyncMock(return_value=False))

        r = await client.delete("/games/types/999")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Тип игры не найден"
