from app.dao.base import BaseDAO
from app.team.models import Team, TeamMember


class TeamDAO(BaseDAO):
    model = Team


class TeamMemberDAO(BaseDAO):
    model = TeamMember
