from typing import Dict, List

from loguru import logger
from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, chat_id: int, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = []
        self.active_connections[chat_id].append(websocket)

    def disconnect(self, chat_id: int, websocket: WebSocket):
        if chat_id in self.active_connections:
            self.active_connections[chat_id].remove(websocket)
            if not self.active_connections[chat_id]:  # Если больше нет участников
                del self.active_connections[chat_id]

    async def broadcast(self, chat_id: int, message: str):
        if chat_id in self.active_connections:
            for connection in self.active_connections[chat_id]:
                await connection.send_text(message)


# class ConnectionManager:
#     def __init__(self):
#         # Хранение активных соединений в виде {chat_id: {user_id: WebSocket}}
#         self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
#
#     async def connect(self, websocket: WebSocket, chat_id: int, user_id: int):
#         """
#         Устанавливает соединение с пользователем.
#         websocket.accept() — подтверждает подключение.
#         """
#         logger.info("Подключаю пользователя={} в чат={}", user_id, chat_id)
#         await websocket.accept()
#         if chat_id not in self.active_connections:
#             self.active_connections[chat_id] = {}
#         self.active_connections[chat_id][user_id] = websocket
#
#     def disconnect(self, chat_id: int, user_id: int):
#         """
#         Закрывает соединение и удаляет его из списка активных подключений.
#         Если в комнате больше нет пользователей, удаляет комнату.
#         """
#         logger.info("Отключаю пользователя={} в чат={}", user_id, chat_id)
#         if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
#             del self.active_connections[chat_id][user_id]
#             if not self.active_connections[chat_id]:
#                 logger.info("Больше нет подключений в чате={}, удаляем его", chat_id)
#                 del self.active_connections[chat_id]
#
#     async def broadcast(self, message: str, chat_id: int, sender_id: int):
#         """
#         Рассылает сообщение всем пользователям в комнате.
#         """
#         logger.info("Уведомляем пользователей чата={}, отправитель={}", chat_id, sender_id)
#         if chat_id in self.active_connections:
#             for user_id, connection in self.active_connections[chat_id].items():
#                 message_with_class = {
#                     "text": message,
#                     "is_self": user_id == sender_id
#                 }
#                 await connection.send_json(message_with_class)


manager = ConnectionManager()
