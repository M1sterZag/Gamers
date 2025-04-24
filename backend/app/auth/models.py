from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.dao.database import Base
from sqlalchemy import Boolean, Date, Integer, String, text


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=True)
    avatar: Mapped[str] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[Date] = mapped_column(Date, server_default=text("CURRENT_DATE"))

    messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    owned_teams = relationship("Team", back_populates="owner", cascade="all, delete-orphan")
    team_memberships = relationship("TeamMember", back_populates="member", cascade="all, delete-orphan")
    chat_memberships = relationship("ChatMember", back_populates="user", cascade="all, delete-orphan")
