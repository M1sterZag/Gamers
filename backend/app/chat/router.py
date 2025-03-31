from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.dao import ChatDAO
from app.chat.models import Message
from app.chat.web_socket_manager import manager
from app.dao.dependencies import get_session_with_commit

router = APIRouter()


@router.websocket("/{team_id}")
async def chat_websocket(
        websocket: WebSocket,
        team_id: int,
        session: AsyncSession = Depends(get_session_with_commit)
):
    chat = await ChatDAO.get_chat_by_team_id(team_id, session)
    if not chat:
        await websocket.close()
        raise HTTPException(status_code=404, detail="Чат не найден")

    await manager.connect(chat.id, websocket)

    try:
        while True:
            data = await websocket.receive_text()
            message = Message(chat_id=chat.id, content=data)
            session.add(message)  # ????
            await session.commit()  # ????
            await manager.send_message(chat.id, data)
    except Exception as e:
        print(f"Ошибка WebSocket: {e}")
    finally:
        await manager.disconnect(chat.id, websocket)
