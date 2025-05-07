from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.auth.dependencies import get_current_admin_user
from app.game.schemas import SGameCreate, SGameRead, SGameTypeCreate, SGameTypeRead
from app.game.dao import GameDAO, GameTypeDAO
from app.dao.dependencies import get_session_with_commit, get_session_without_commit

router = APIRouter()


@router.post("")
async def create_game(
        game_data: SGameCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    return await GameDAO.add(session=session, **game_data.model_dump())


@router.get("")
async def read_games(session: AsyncSession = Depends(get_session_without_commit)):
    return await GameDAO.find_all(session=session)


@router.put("/{game_id}")
async def update_game(
        game_id: int,
        game_data: SGameCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    updated_count = await GameDAO.update(
        filter_by={"id": game_id},
        session=session,
        **game_data.model_dump()
    )
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Игра не найдена")

    return {"message": "success"}


@router.delete("/{game_id}")
async def delete_game(
        game_id: int,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    deleted = await GameDAO.delete(session=session, id=game_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Игра не найдена")
    return {"message": "Игра успешно удалена"}


# CRUD для типов игр
@router.post("/types")
async def create_game_type(
        game_type_data: SGameTypeCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    return await GameTypeDAO.add(session=session, **game_type_data.model_dump())


@router.get("/types")
async def read_game_types(session: AsyncSession = Depends(get_session_without_commit)):
    return await GameTypeDAO.find_all(session=session)


@router.put("/types/{game_type_id}")
async def update_game_type(
        game_type_id: int,
        game_type_data: SGameTypeCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    # Исправленный вызов update с правильными параметрами
    updated_count = await GameTypeDAO.update(
        filter_by={"id": game_type_id},
        session=session,
        **game_type_data.model_dump()
    )
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Тип игры не найден")

    return {"message": "success"}


@router.delete("/types/{game_type_id}")
async def delete_game_type(
        game_type_id: int,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    deleted = await GameTypeDAO.delete(session=session, id=game_type_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Тип игры не найден")
    return {"message": "Тип игры успешно удален"}
