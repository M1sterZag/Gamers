from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.auth.schemas import SUserRead
from app.chat.dao import ChatDAO, ChatMemberDAO
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.team.dao import TeamDAO, TeamMemberDAO
from app.team.models import TeamMember
from app.team.schemas import STeamCreate, STeamRead

router = APIRouter()


@router.post("/")
async def create_team(team_data: STeamCreate,
                      current_user: SUserRead = Depends(get_current_active_user),
                      session: AsyncSession = Depends(get_session_with_commit)):
    new_chat = await ChatDAO.add(
        session=session,
        name=team_data.name,
        owner_id=current_user.id,
    )

    new_team = await TeamDAO.add(
        session=session,
        name=team_data.name,
        game_id=team_data.game_id,
        description=team_data.description,
        max_members=team_data.max_members,
        owner_id=current_user.id,
        chat_id=new_chat.id,
        game_type_id=team_data.game_type_id,
        time=team_data.time,
    )

    await TeamMemberDAO.add(
        session=session,
        user_id=current_user.id,
        team_id=new_team.id,
    )

    await ChatMemberDAO.add(
        session=session,
        chat_id=new_chat.id,
        user_id=current_user.id,
    )

    return {
        "message": "Команда успешно создана",
        "team_id": new_team.id,
        "chat_id": new_chat.id
    }


@router.get("/")
async def read_teams(session: AsyncSession = Depends(get_session_without_commit)) -> List[STeamRead]:
    return await TeamDAO.find_all(session=session)


@router.get("/{team_id}")
async def read_team(team_id: int, session: AsyncSession = Depends(get_session_without_commit)) -> List[STeamRead]:
    return await TeamDAO.find_one_or_none_by_id(session=session, data_id=team_id)


@router.delete("/{team_id}")
async def delete_team(
        team_id: int,
        current_user: SUserRead = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_session_with_commit),
):
    team = await TeamDAO.find_one_or_none(session=session, id=team_id, owner_id=current_user.id)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена или вы не являетесь владельцем")

    await TeamDAO.delete(session=session, id=team_id)

    return {"message": "Команда и все связанные данные успешно удалены"}


# TODO добавить человека в websocket чата
@router.post("/member/{team_id}")
async def create_team_member(
        team_id: int,
        current_user: SUserRead = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_session_with_commit)):
    # Находим команду по ID
    team = await TeamDAO.find_one_or_none_by_id(session=session, data_id=team_id)
    if not team:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Команда не найдена"
        )

    # Проверяем, не является ли пользователь уже участником команды
    existing_member = await TeamMemberDAO.find_one_or_none(
        session=session,
        team_id=team_id,
        user_id=current_user.id
    )
    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь уже является участником команды"
        )

    # Получаем текущее количество участников команды
    current_members_count = await session.execute(
        select(func.count()).where(TeamMember.team_id == team_id)
    )
    current_members_count = current_members_count.scalar()

    # Проверяем, не превышено ли максимальное количество участников
    if current_members_count == team.max_members:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Команда уже заполнена"
        )

    # Добавляем пользователя в команду
    await TeamMemberDAO.add(session=session, user_id=current_user.id, team_id=team_id)

    # Добавляем пользователя в чат команды
    await ChatMemberDAO.add(session=session, user_id=current_user.id, chat_id=team.chat_id)

    return {"message": "Пользователь успешно добавлен в команду"}


@router.delete("/member/{team_id}")
async def delete_team_member(
        team_id: int,
        user_id: int = None,
        current_user: SUserRead = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_session_with_commit),
):
    # Находим команду по ID
    team = await TeamDAO.find_one_or_none_by_id(team_id, session)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")

    # Если user_id не указан, удаляем текущего пользователя
    if user_id is None:
        user_id = current_user.id

    # Проверяем, является ли текущий пользователь владельцем команды
    if team.owner_id == current_user.id:
        if user_id == current_user.id:
            # Владелец не может удалить себя из команды
            raise HTTPException(
                status_code=403,
                detail="Владелец не может удалить себя из команды. Используйте endpoint для удаления команды."
            )
        else:
            # Владелец может удалить других участников
            deleted_count = await TeamMemberDAO.delete(session, team_id=team_id, user_id=user_id)
    else:
        # Обычный участник может удалить только себя
        if user_id != current_user.id:
            raise HTTPException(
                status_code=403,
                detail="Вы можете удалить только себя из команды"
            )
        deleted_count = await TeamMemberDAO.delete(session, team_id=team_id, user_id=user_id)

    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Участник не найден в команде")

    return {"message": "Участник успешно удален из команды"}
