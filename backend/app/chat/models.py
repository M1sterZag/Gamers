from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, text, Date, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.dao.database import Base


class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="messages", lazy="joined")


class Chat(Base):
    __tablename__ = 'chats'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('teams.id', ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(Date, server_default=text("CURRENT_DATE"))

    team = relationship("Team", back_populates="chat", uselist=False)
    members = relationship("ChatMember", back_populates="chat", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")


class ChatMember(Base):
    __tablename__ = 'chat_members'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey("chats.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")
