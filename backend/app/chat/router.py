import json
from datetime import datetime

from fastapi import APIRouter, WebSocket, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.websockets import WebSocketDisconnect

from app.auth.dependencies import get_current_active_user_from_token
from app.chat.dao import ChatDAO, MessageDAO
from app.chat.web_socket_manager import manager
from app.dao.dependencies import get_session_with_commit

router = APIRouter()


@router.websocket("/{team_id}")
async def websocket_endpoint(websocket: WebSocket, team_id: int,
                             session: AsyncSession = Depends(get_session_with_commit)):
    chat = await ChatDAO.find_one_or_none(session=session, team_id=team_id)
    chat_id = chat.id
    # Извлекаем access_token из cookies WebSocket
    access_token = websocket.cookies.get("access_token")
    if not access_token:
        logger.error("Access token not found in WebSocket cookies")
        await websocket.close(code=4001, reason="No access token provided")
        return

    try:
        # Проверяем токен и получаем текущего пользователя
        current_user = await get_current_active_user_from_token(access_token, session)
    except Exception as e:
        logger.error(f"Error validating user: {str(e)}")
        await websocket.close(code=4001, reason="Invalid token")
        return

    # Подключаем пользователя к чату
    await manager.connect(chat_id, websocket)

    try:
        message_history = await MessageDAO.find_all(session=session, chat_id=chat_id)
        logger.info(f"Получено сообщений: {len(message_history)}")
        for msg in message_history:
            await websocket.send_text(json.dumps({
                "content": msg.content,
                "sender_id": msg.sender_id,
                "created_at": msg.created_at.strftime("%H:%M"),
                "is_sender": msg.sender_id == current_user.id
            }))

        while True:
            data = await websocket.receive_text()
            created_at = datetime.now()
            new_message = await MessageDAO.add(
                session=session,
                sender_id=current_user.id,
                chat_id=chat_id,
                content=data,
                created_at=created_at
            )
            formatted_time = created_at.strftime("%H:%M")
            await manager.broadcast(chat_id, json.dumps({
                "content": data,
                "sender_id": current_user.id,
                "created_at": formatted_time,
                "is_sender": True
            }))
    except WebSocketDisconnect:
        await manager.disconnect(chat_id, websocket)
    except Exception as e:
        logger.error(f"Поймана ошибка: {e}")
        logger.exception("Stack trace:")
    finally:
        await manager.disconnect(chat_id, websocket)
