from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, String, Date, text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


# TODO продумать логику удаление команд с прошедшим временем
# TODO каскадное удаление команд при удалении пользователей
class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    game_id: Mapped[int] = mapped_column(Integer, ForeignKey('games.id'), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    max_members: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(Date, server_default=text("CURRENT_DATE"))
    game_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('game_types.id'), nullable=False)
    time: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    chat = relationship("Chat", back_populates="team", uselist=False, cascade="all, delete-orphan")
    members = relationship("TeamMember", back_populates="team", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint('time >= CURRENT_TIMESTAMP', name='check_time_in_future'),
    )


class TeamMember(Base):
    __tablename__ = 'team_members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id', ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    joined_at: Mapped[datetime] = mapped_column(Date, server_default=text("CURRENT_DATE"))

    team = relationship("Team", back_populates="members")
    user = relationship("User")
