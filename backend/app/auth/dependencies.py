from datetime import datetime, timezone
from fastapi import Request, Depends
import jwt
from jose import JWTError
from jwt import ExpiredSignatureError
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.auth.models import User
from app.config import settings
from app.dao.dependencies import get_session_without_commit
from app.exceptions import (
    TokenNoFoundException, NoJwtException, TokenExpiredException, NoUserIdException, ForbiddenException,
    UserNotFoundException, AccountIsNotActiveException
)


def get_access_token(request: Request) -> str:
    """Извлекаем access_token из кук."""
    token = request.cookies.get('access_token')
    logger.info("Пытаюсь извлечь токен авторизации")
    if not token:
        raise TokenNoFoundException
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get('refresh_token')
    logger.info("Пытаюсь извлечь токен обновления")
    if not token:
        raise TokenNoFoundException
    return token


async def check_refresh_token(
        token: str = Depends(get_refresh_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """ Проверяем refresh_token и возвращаем пользователя."""
    try:
        logger.info("Проверка рефреш токена")
        payload = jwt.decode(
            token,
            settings.auth_jwt.public_key,  # settings.auth_jwt.SECRET_KEY
            algorithms=[settings.auth_jwt.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise NoJwtException

        user = await UsersDAO.find_one_or_none_by_id(session=session, data_id=int(user_id))
        if not user:
            raise NoJwtException

        return user
    except JWTError:
        raise NoJwtException


async def get_current_user(
        token: str = Depends(get_access_token),
        session: AsyncSession = Depends(get_session_without_commit)
) -> User:
    """Проверяем access_token и возвращаем пользователя"""
    return await _verify_token_and_get_user(token, session)


async def get_current_active_user_from_token(
        token: str,
        session: AsyncSession
) -> User:
    """Проверяем access_token из WebSocket и возвращаем активного пользователя"""
    return await _verify_token_and_get_user(token, session, check_active=True)


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Проверяем права пользователя как администратора."""
    logger.info("Проверка на права администратора")
    if current_user.is_admin and current_user.is_active:
        return current_user
    raise ForbiddenException


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    logger.info("Проверка пользователя на блокировку")
    if current_user.is_active:
        return current_user
    raise AccountIsNotActiveException


async def _verify_token_and_get_user(
        token: str,
        session: AsyncSession,
        check_active: bool = False
) -> User:
    """Общая функция для проверки токена и получения пользователя"""
    try:
        logger.info("Проверка токена")
        payload = jwt.decode(token, settings.auth_jwt.public_key, algorithms=[settings.auth_jwt.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise NoJwtException

    # Проверка срока действия
    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    # Получение user_id
    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    # Поиск пользователя
    user = await UsersDAO.find_one_or_none_by_id(session=session, data_id=int(user_id))
    if not user:
        raise UserNotFoundException

    # Дополнительная проверка активности
    if check_active and not user.is_active:
        raise AccountIsNotActiveException

    return user
