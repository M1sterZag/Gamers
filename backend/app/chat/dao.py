from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.chat.models import Chat, Message, ChatMember
from app.dao.base import BaseDAO


class ChatDAO(BaseDAO):
    model = Chat
    
    @staticmethod
    async def get_chat_by_team_id(team_id: int, session: AsyncSession):
        query = select(Chat).filter_by(team_id=team_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    async def create_chat(team_id: int, session: AsyncSession):
        chat = Chat(team_id=team_id)
        session.add(chat)
        await session.commit()
        return chat


class ChatMemberDAO(BaseDAO):
    model = ChatMember


class MessageDAO(BaseDAO):
    model = Message

    @staticmethod
    async def save_message(chat_id: int, content: str, session: AsyncSession):
        message = Message(chat_id=chat_id, content=content)
        session.add(message)
        await session.commit()
        return message

    @staticmethod
    async def get_messages(chat_id: int, session: AsyncSession):
        query = select(Message).filter_by(chat_id=chat_id).order_by(Message.timestamp)
        result = await session.execute(query)
        return result.scalars().all()
