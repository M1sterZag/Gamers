from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Text, DateTime, String, Date, text
from sqlalchemy.orm import Mapped, mapped_column

from app.dao.database import Base


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('game.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    max_members: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(Date, server_default=text("CURRENT_DATE"))
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chat.id'), nullable=False)
    game_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('game_type.id'), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)


class TeamMember(Base):
    __tablename__ = 'team_members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('team.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(Date, server_default=text("CURRENT_DATE"))
