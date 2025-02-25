from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.auth.schemas import SUserRead
from app.chat.dao import ChatMemberDAO, MessageDAO
from app.chat.web_socket_manager import manager
from app.dao.dependencies import get_session_with_commit

router = APIRouter()


@router.websocket("/{chat_id}")
async def websocket_endpoint(
        websocket: WebSocket,
        chat_id: int,
        current_user: SUserRead = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    # Проверяем, является ли пользователь участником чата
    chat_member = await ChatMemberDAO.find_one_or_none(
        session=session, chat_id=chat_id, user_id=current_user.id
    )
    if not chat_member:
        await websocket.close(code=1008)  # Код для запрета доступа
        raise HTTPException(status_code=403, detail="Вы не участник этого чата")

    await manager.connect(chat_id, websocket)

    # Отправляем историю чата
    chat_history = await MessageDAO.get_chat_history(session=session, chat_id=chat_id)
    for message in reversed(chat_history):
        await websocket.send_text(f"{message.user_id}: {message.content}")

    # Основной цикл общения
    try:
        while True:
            data = await websocket.receive_text()

            # Сохраняем сообщение в БД
            saved_message = await MessageDAO.add(
                session=session,
                chat_id=chat_id,
                sender_id=current_user.id,
                content=data
            )

            # Отправляем сообщение всем участникам чата
            await manager.broadcast(chat_id, f"{current_user.username}: {data}")

    except Exception as e:
        print(f"Ошибка соединения: {e}")
    finally:
        manager.disconnect(chat_id, websocket)
