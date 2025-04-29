from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_active_user
from app.auth.schemas import SUserRead
from app.chat.dao import ChatDAO, ChatMemberDAO
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.game.dao import GameDAO, GameTypeDAO
from app.team.dao import TeamDAO, TeamMemberDAO
from app.team.models import TeamMember
from app.team.schemas import STeamCreate, STeamRead
from app.auth.dao import UsersDAO

router = APIRouter()


@router.post("")
async def create_team(team_data: STeamCreate,
                      current_user: SUserRead = Depends(get_current_active_user),
                      session: AsyncSession = Depends(get_session_with_commit)):
    try:
        async with session.begin():  # Начинаем транзакцию вручную

            # Создаем команду с привязкой к чату
            new_team = await TeamDAO.add(
                session=session,
                name=team_data.name,
                game_id=team_data.game_id,
                description=team_data.description,
                max_members=team_data.max_members,
                owner_id=current_user.id,
                game_type_id=team_data.game_type_id,
                time=team_data.time,
            )

            # Создаем чат
            new_chat = await ChatDAO.add(
                session=session,
                name=team_data.name,
                team_id=new_team.id,
            )

            # Добавляем создателя команды в команду
            await TeamMemberDAO.add(
                session=session,
                user_id=current_user.id,
                team_id=new_team.id,
            )

            # Добавляем создателя в чат
            await ChatMemberDAO.add(
                session=session,
                chat_id=new_chat.id,
                user_id=current_user.id,
            )

        # Если все операции успешны, транзакция будет зафиксирована
        return {
            "message": "Команда и чат успешно созданы",
            "team_id": new_team.id,
            "chat_id": new_chat.id
        }

    except Exception as e:
        # В случае ошибки транзакция откатывается
        logger.error(f"Ошибка при создании команды: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при создании команды")


@router.get("")
async def read_teams(session: AsyncSession = Depends(get_session_without_commit)) -> List[STeamRead]:
    # Получаем все команды
    teams = await TeamDAO.find_all(session=session)

    # Формируем результат
    result = []
    for team in teams:
        # Для каждой команды получаем участников отдельным запросом
        members = await TeamMemberDAO.find_all(session=session, team_id=team.id)

        team_data = team.__dict__
        team_data['members'] = members
        result.append(STeamRead(**team_data))

    return result


@router.get("/{team_id}")
async def read_team(
        team_id: int,
        session: AsyncSession = Depends(get_session_without_commit)
):
    try:
        # Получаем команду
        team = await TeamDAO.find_one_or_none_by_id(session=session, data_id=team_id)
        if not team:
            raise HTTPException(status_code=404, detail="Команда не найдена")

        # Получаем участников команды
        members = await TeamMemberDAO.find_all(session, team_id=team_id)

        # Получаем информацию о пользователях
        members_with_users = []
        for member in members:
            user = await UsersDAO.find_one_or_none_by_id(session=session, data_id=member.user_id)
            members_with_users.append({
                "id": member.id,
                "user_id": member.user_id,
                "username": user.username if user else "Unknown",
                "joined_at": member.joined_at
            })

        # Получаем информацию об игре и типе игры
        game = await GameDAO.find_one_or_none_by_id(session=session, data_id=team.game_id)
        game_type = await GameTypeDAO.find_one_or_none_by_id(session=session, data_id=team.game_type_id)

        return {
            "id": team.id,
            "name": team.name,
            "description": team.description,
            "game_id": team.game_id,
            "game": game.name if game else "Unknown",
            "game_type_id": team.game_type_id,
            "gameType": game_type.name if game_type else "Unknown",
            "max_members": team.max_members,
            "time": team.time,
            "owner_id": team.owner_id,
            "created_at": team.created_at,
            "members": members_with_users
        }

    except Exception as e:
        logger.error(f"Ошибка при получении команды: {str(e)}")
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")


@router.delete("/{team_id}")
async def delete_team(
        team_id: int,
        current_user: SUserRead = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_session_with_commit),
):
    """
    Удаляет команду. Только владелец команды или администратор могут её удалить.
    """
    # Находим команду по ID
    team = await TeamDAO.find_one_or_none_by_id(session=session, data_id=team_id)
    if not team:
        raise HTTPException(status_code=404, detail="Команда не найдена")

    # Проверяем права пользователя
    if not current_user.is_admin and team.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="У вас нет прав для удаления этой команды")

    # Удаляем команду
    await TeamDAO.delete(session=session, id=team_id)
    return {"message": "Команда и все связанные данные успешно удалены"}


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

    # Ищем чат и добавляем пользователя в чат команды
    chat = await ChatDAO.find_one_or_none(session=session, team_id=team.id)
    if chat:
        await ChatMemberDAO.add(session=session, user_id=current_user.id, chat_id=chat.id)
        return {"message": "Пользователь успешно добавлен в команду"}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Чат команды не найден"
        )


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


@router.get("/recent/{user_id}")
async def get_user_recent_teams(
        user_id: int,
        session: AsyncSession = Depends(get_session_without_commit)
):
    """
    Получает последние команды пользователя

    Args:
        user_id: ID пользователя
        session: Асинхронная сессия SQLAlchemy

    Returns:
        Список последних команд пользователя
    """
    try:
        # Получаем команды пользователя
        teams = await TeamMemberDAO.find_user_teams(session=session, user_id=user_id)

        # Формируем результат
        result = []
        for team in teams:
            # Получаем количество участников для каждой команды
            members_count = await session.execute(
                select(func.count()).where(TeamMember.team_id == team.id)
            )
            members_count = members_count.scalar()

            # Получаем информацию об игре
            game = await GameDAO.find_one_or_none_by_id(session=session, data_id=team.game_id)
            game_type = await GameTypeDAO.find_one_or_none_by_id(session=session, data_id=team.game_type_id)

            team_data = {
                "id": team.id,
                "name": team.name,
                "game": game.name if game else "Unknown",
                "game_type": game_type.name if game_type else "Unknown",
                "time": team.time,
                "members_count": members_count,
                "owner_id": team.owner_id
            }
            result.append(team_data)

        return result

    except Exception as e:
        logger.error(f"Ошибка при получении команд пользователя: {str(e)}")
        raise HTTPException(status_code=500, detail="Ошибка при получении списка команд")
