from loguru import logger
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.responses import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.config import settings


def create_tokens(data: dict) -> dict:
    logger.info("Создание новых токенов")
    # Текущее время в UTC
    now = datetime.now(timezone.utc)

    # AccessToken - 30 минут
    access_expire = now + timedelta(settings.auth_jwt.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_payload = data.copy()
    access_payload.update({"exp": int(access_expire.timestamp()), "type": "access"})
    access_token = jwt.encode(
        access_payload,
        settings.auth_jwt.SECRET_KEY,
        algorithm=settings.auth_jwt.ALGORITHM
    )

    # RefreshToken - 7 дней
    refresh_expire = now + timedelta(days=7)
    refresh_payload = data.copy()
    refresh_payload.update({"exp": int(refresh_expire.timestamp()), "type": "refresh"})
    refresh_token = jwt.encode(
        refresh_payload,
        settings.auth_jwt.SECRET_KEY,
        algorithm=settings.auth_jwt.ALGORITHM
    )
    return {"access_token": access_token, "refresh_token": refresh_token}


async def authenticate_user(session: AsyncSession, email: EmailStr, password: str):
    logger.info("Аутентификация пользователя")
    user = await UsersDAO.find_one_or_none(session=session, email=email)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user


def set_tokens(response: Response, user_id: int):
    logger.info("Установка токенов")
    new_tokens = create_tokens(data={"sub": str(user_id)})
    access_token = new_tokens.get('access_token')
    refresh_token = new_tokens.get("refresh_token")

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # True если https
        domain="gamers-team.ru",  # нужно обновить домен
        samesite="lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,  # True если https
        domain="gamers-team.ru",  # нужно обновить домен
        samesite="lax"
    )


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    logger.info("Получение хеша пароля")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    logger.info("Проверка пароля")
    return pwd_context.verify(plain_password, hashed_password)
