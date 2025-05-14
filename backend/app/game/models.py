from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)


class GameType(Base):
    __tablename__ = 'game_types'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
