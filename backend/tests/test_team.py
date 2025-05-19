import pytest
from types import SimpleNamespace
from unittest.mock import AsyncMock
from fastapi import status

from app.team.dao import TeamDAO, TeamMemberDAO
from app.chat.dao import ChatDAO, ChatMemberDAO
from app.auth.dao import UsersDAO
from app.game.dao import GameDAO, GameTypeDAO

TEAM_CREATE = {
    "name": "Alpha Team",
    "game_id": 1,
    "game_type_id": 2,
    "description": "A cool team",
    "max_members": 5,
    "time": "2099-12-31T12:00:00"
}


@pytest.mark.anyio
class TestTeamAPI:

    async def test_create_team_success(self, client, monkeypatch, fake_user):
        monkeypatch.setattr(TeamDAO, "add", AsyncMock(return_value=SimpleNamespace(id=10)))
        monkeypatch.setattr(ChatDAO, "add", AsyncMock(return_value=SimpleNamespace(id=20)))
        monkeypatch.setattr(TeamMemberDAO, "add", AsyncMock())
        monkeypatch.setattr(ChatMemberDAO, "add", AsyncMock())

        r = await client.post("/teams", json=TEAM_CREATE)
        assert r.status_code == status.HTTP_200_OK
        data = r.json()
        assert data["message"] == "Команда и чат успешно созданы"
        assert data["team_id"] == 10
        assert data["chat_id"] == 20

    async def test_read_teams(self, client, monkeypatch):
        team_obj = SimpleNamespace(
            id=1, name="T1", game_id=1, game_type_id=1,
            description="desc", max_members=3,
            time="2099-01-01T00:00:00", owner_id=1,
            created_at="2099-01-01T00:00:00"
        )
        member_obj = SimpleNamespace(
            id=5, team_id=1, user_id=1,
            joined_at="2099-01-01T00:00:00"
        )

        monkeypatch.setattr(TeamDAO, "find_all", AsyncMock(return_value=[team_obj]))
        monkeypatch.setattr(TeamMemberDAO, "find_all", AsyncMock(return_value=[member_obj]))

        r = await client.get("/teams")
        assert r.status_code == status.HTTP_200_OK
        result = r.json()
        assert isinstance(result, list) and len(result) == 1
        members = result[0]["members"]
        assert members[0]["team_id"] == 1
        assert members[0]["user_id"] == 1

    async def test_read_team_detail_success(self, client, monkeypatch):
        team = SimpleNamespace(
            id=2, name="T2", game_id=1, game_type_id=2,
            description="desc2", max_members=4,
            time="2099-06-01T12:00:00", owner_id=1,
            created_at="2099-06-01T12:00:00"
        )
        member = SimpleNamespace(
            id=7, team_id=2, user_id=1,
            joined_at="2099-06-01T12:00:00"
        )

        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=team))
        monkeypatch.setattr(TeamMemberDAO, "find_all", AsyncMock(return_value=[member]))
        monkeypatch.setattr(UsersDAO, "find_one_or_none_by_id",
                            AsyncMock(return_value=SimpleNamespace(username="user1")))
        monkeypatch.setattr(GameDAO, "find_one_or_none_by_id",
                            AsyncMock(return_value=SimpleNamespace(name="GameX")))
        monkeypatch.setattr(GameTypeDAO, "find_one_or_none_by_id",
                            AsyncMock(return_value=SimpleNamespace(name="TypeY")))

        r = await client.get("/teams/2")
        assert r.status_code == status.HTTP_200_OK
        d = r.json()
        assert d["id"] == 2
        assert d["game"] == "GameX"
        assert d["gameType"] == "TypeY"
        assert isinstance(d["members"], list)

    async def test_read_team_not_found(self, client, monkeypatch):
        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=None))

        r = await client.get("/teams/999")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Команда не найдена"

    async def test_delete_team_success(self, client, monkeypatch, fake_user):
        team = SimpleNamespace(owner_id=fake_user.id)
        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=team))
        mock_del = AsyncMock(return_value=True)
        monkeypatch.setattr(TeamDAO, "delete", mock_del)

        r = await client.delete("/teams/1")
        assert r.status_code == status.HTTP_200_OK
        assert "Команда и все связанные данные" in r.json()["message"]

    async def test_delete_team_forbidden(self, client, monkeypatch, fake_user):
        fake_user.is_admin = False
        team = SimpleNamespace(owner_id=999)
        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=team))

        r = await client.delete("/teams/1")
        assert r.status_code == status.HTTP_403_FORBIDDEN
        assert r.json()["detail"] == "У вас нет прав для удаления этой команды"

    async def test_delete_team_not_found(self, client, monkeypatch, fake_user):
        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=None))

        r = await client.delete("/teams/123")
        assert r.status_code == status.HTTP_404_NOT_FOUND
        assert r.json()["detail"] == "Команда не найдена"

    async def test_create_team_member_success(self, client, monkeypatch, fake_session, fake_user):
        team = SimpleNamespace(id=3, max_members=2)
        monkeypatch.setattr(TeamDAO, "find_one_or_none_by_id", AsyncMock(return_value=team))
        monkeypatch.setattr(TeamMemberDAO, "find_one_or_none", AsyncMock(return_value=None))

        session_exec = AsyncMock()
        session_exec.return_value.scalar = AsyncMock(return_value=1)
        fake_session.execute = session_exec

        monkeypatch.setattr(TeamMemberDAO, "add", AsyncMock())
        monkeypatch.setattr(ChatDAO, "find_one_or_none", AsyncMock(return_value=SimpleNamespace(id=5)))
        monkeypatch.setattr(ChatMemberDAO, "add", AsyncMock())

        r = await client.post("/teams/member/3")
        assert r.status_code == status.HTTP_200_OK
        assert r.json()["message"] == "Пользователь успешно добавлен в команду"
