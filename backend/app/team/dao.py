from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.team.models import Team, TeamMember


class TeamDAO(BaseDAO):
    model = Team


class TeamMemberDAO(BaseDAO):
    model = TeamMember

    @classmethod
    async def find_user_teams(
            cls,
            session: AsyncSession,
            user_id: int,
            limit: int = 5
    ):
        """
        Находит последние команды пользователя

        Args:
            session: Асинхронная сессия SQLAlchemy
            user_id: ID пользователя
            limit: Максимальное количество возвращаемых команд

        Returns:
            Список команд пользователя, отсортированный по дате вступления (новые сначала)
        """
        stmt = (
            select(Team)
            .join(TeamMember, TeamMember.team_id == Team.id)
            .where(TeamMember.user_id == user_id)
            .order_by(TeamMember.joined_at.desc())
            .limit(limit)
        )
        result = await session.execute(stmt)
        return result.scalars().all()
