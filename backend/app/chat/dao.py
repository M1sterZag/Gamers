from app.dao.base import BaseDAO
from app.chat.models import Chat, ChatMember, Message


class ChatDAO(BaseDAO):
    model = Chat


class ChatMemberDAO(BaseDAO):
    model = ChatMember


class MessageDAO(BaseDAO):
    model = Message
