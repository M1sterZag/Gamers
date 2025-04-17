from authlib.jose import jwt
from fastapi import APIRouter, WebSocket, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from app.auth.dependencies import get_current_active_user
from app.auth.schemas import SUserRead
from app.chat.dao import ChatDAO, MessageDAO
from app.chat.web_socket_manager import manager
from app.config import settings
from app.dao.dependencies import get_session_with_commit, get_session_without_commit

router = APIRouter()


@router.websocket("/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int):
    await manager.connect(chat_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(chat_id, data)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await manager.disconnect(chat_id, websocket)

# @router.websocket("/ws/chats/{chat_id}")
# async def chat_websocket(
#         websocket: WebSocket,
#         chat_id: int,
#         session: AsyncSession = Depends(get_session_with_commit),
# ):
#     # Извлекаем токен из параметров запроса
#     query_params = websocket.query_params
#     token = query_params.get("token")
#
#     if not token:
#         await websocket.close(code=4001, reason="Missing token")
#         return
#
#     try:
#         # Декодируем токен
#         payload = jwt.decode(token, settings.auth_jwt.SECRET_KEY, algorithms=[settings.auth_jwt.ALGORITHM])
#         user_id = payload.get("sub")
#         if not user_id:
#             await websocket.close(code=4001, reason="Invalid token")
#             return
#     except Exception as e:
#         logger.info("Неправильный токен")
#         await websocket.close(code=4001, reason="Invalid token")
#         return
#
#     # Подключаем пользователя к чату
#     await manager.connect(chat_id, websocket, user_id)
#
#     try:
#         while True:
#             data = await websocket.receive_text()
#             # Сохраняем сообщение в базу данных
#             await MessageDAO.add(
#                 session=session,
#                 chat_id=chat_id,
#                 content=data,
#                 sender_id=user_id,  # ID текущего пользователя
#             )
#             # Отправляем сообщение всем участникам чата
#             await manager.send(data, chat_id, user_id)
#
#     except WebSocketDisconnect:
#         logger.info("Отключение от вебсокета")
#         manager.disconnect(chat_id, websocket)
