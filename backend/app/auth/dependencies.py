from datetime import datetime, timezone
from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError
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
    token = request.cookies.get('user_access_token')
    logger.info("Пытаюсь извлечь токен авторизации")
    if not token:
        raise TokenNoFoundException
    return token


def get_refresh_token(request: Request) -> str:
    """Извлекаем refresh_token из кук."""
    token = request.cookies.get('user_refresh_token')
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
            settings.auth_jwt.SECRET_KEY,
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
    """Проверяем access_token и возвращаем пользователя."""
    try:
        # Декодируем токен
        logger.info("Проверка текущего пользователя")
        payload = jwt.decode(token, settings.auth_jwt.SECRET_KEY, algorithms=[settings.auth_jwt.ALGORITHM])
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        # Общая ошибка для токенов
        raise NoJwtException

    expire: str = payload.get('exp')
    expire_time = datetime.fromtimestamp(int(expire), tz=timezone.utc)
    if (not expire) or (expire_time < datetime.now(timezone.utc)):
        raise TokenExpiredException

    user_id: str = payload.get('sub')
    if not user_id:
        raise NoUserIdException

    user = await UsersDAO.find_one_or_none_by_id(session=session, data_id=int(user_id))
    if not user:
        raise UserNotFoundException
    return user


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
