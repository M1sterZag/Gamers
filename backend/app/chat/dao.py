from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.chat.models import Chat, ChatMember, Message


class ChatDAO(BaseDAO):
    model = Chat


class ChatMemberDAO(BaseDAO):
    model = ChatMember


class MessageDAO(BaseDAO):
    model = Message

    @classmethod
    async def get_chat_history(cls, session: AsyncSession, chat_id: int, limit: int = 50):
        query = select(cls.model).where(cls.model.chat_id == chat_id).order_by(cls.model.created_at.desc()).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()
