from typing import List
from fastapi import APIRouter, Response, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.auth.utils import authenticate_user, set_tokens
from app.auth.dependencies import get_current_user, get_current_admin_user, check_refresh_token
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException, AccountIsNotActiveException
from app.auth.dao import UsersDAO
from app.auth.schemas import SUserRegister, SUserAuth, SUserRead, SUserUpdate

router = APIRouter()


@router.post("/register")
async def register_user(user_data: SUserRegister, session: AsyncSession = Depends(get_session_with_commit)) -> dict:
    logger.info("Регистрация пользователя")
    user = await UsersDAO.find_one_or_none(session=session, email=user_data.email)
    if user:
        raise UserAlreadyExistsException

    await UsersDAO.add(
        session=session,
        username=user_data.username,
        email=user_data.email,
        password=user_data.password  # Проверка пароля и хеширование происходит в схеме регистрации
    )

    return {'message': 'Вы успешно зарегистрированы!'}


@router.post("/login")
async def auth_user(
        response: Response,
        user_data: SUserAuth,
        session: AsyncSession = Depends(get_session_without_commit)
) -> dict:
    logger.info("Вход пользователя")
    user = await authenticate_user(session=session, email=user_data.email, password=user_data.password)
    if user is None:
        raise IncorrectEmailOrPasswordException

    if not user.is_active:
        raise AccountIsNotActiveException

    set_tokens(response, user.id)

    return {
        'ok': True,
        'message': 'Авторизация успешна!',
    }


@router.post("/logout")
async def logout(response: Response):
    logger.info("Очистка токенов (выход)")
    # для сервера
    response.delete_cookie(
        key="access_token",
        path="/",
        domain="gamers-team.ru"
    )
    response.delete_cookie(
        key="refresh_token",
        path="/",
        domain="gamers-team.ru"
    )
    # для localhost
    # response.delete_cookie("access_token")
    # response.delete_cookie("refresh_token")
    return {'message': 'Пользователь успешно вышел из системы'}


@router.get("/me")
async def get_me(user_data: User = Depends(get_current_user)) -> SUserRead:
    return SUserRead.model_validate(user_data)


@router.get("/users")
async def get_all_users(admin: User = Depends(get_current_admin_user),
                        session: AsyncSession = Depends(get_session_without_commit)) -> List[SUserRead]:
    return await UsersDAO.find_all(session=session)


@router.post("/refresh")
async def process_refresh_token(
        response: Response,
        user: User = Depends(check_refresh_token)
):
    logger.info("Запуск обновления токенов")
    set_tokens(response, user.id)
    return {"message": "Токены успешно обновлены"}


@router.delete("/users/{user_id}")
async def delete_user_by_id(user_id: int,
                            admin: User = Depends(get_current_admin_user),
                            session: AsyncSession = Depends(get_session_with_commit)):
    deleted = await UsersDAO.delete(session=session, id=user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "Пользователь удален"}


@router.put("/users/{user_id}")
async def update_user_by_id(
        user_id: int,
        user_data: SUserUpdate,
        admin: User = Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    update_data = user_data.model_dump(exclude_unset=True)
    updated_count = await UsersDAO.update(
        filter_by={"id": user_id},
        session=session,
        **update_data
    )
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": "success"}
