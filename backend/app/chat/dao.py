from app.chat.models import Chat, Message, ChatMember
from app.dao.base import BaseDAO


class ChatDAO(BaseDAO):
    model = Chat


class ChatMemberDAO(BaseDAO):
    model = ChatMember


class MessageDAO(BaseDAO):
    model = Message
