from app.dao.base import BaseDAO
from app.game.models import Game, GameType


class GameDAO(BaseDAO):
    model = Game


class GameTypeDAO(BaseDAO):
    model = GameType
