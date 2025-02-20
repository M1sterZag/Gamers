from fastapi import APIRouter, HTTPException, Depends, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dao import UsersDAO
from app.auth.google.setup import oauth
from app.auth.schemas import SUserAddDB, EmailModel
from app.auth.utils import set_tokens
from app.config import settings
from app.dao.dependencies import get_session_with_commit

router = APIRouter()


@router.post("/")
async def auth_google(request: Request):
    return await oauth.google.authorize_redirect(request=request, redirect_uri=settings.google_auth.google_redirect_uri)


@router.get("/callback")
async def auth_google_callback(response: Response, session: AsyncSession = Depends(get_session_with_commit)):
    token = await oauth.google.authorize_access_token()  # Получаем токен
    user_info = await oauth.google.parse_id_token(token)  # Декодируем данные пользователя

    if not user_info:
        raise HTTPException(status_code=400, detail="Ошибка авторизации через Google")

    email = user_info.get("email")
    username = user_info.get("name") or email.split("@")[0]
    # avatar = user_info.get("picture")

    user_dao = UsersDAO(session)

    user = await user_dao.find_one_or_none(filters=EmailModel(email=email))

    if not user:
        user_data = SUserAddDB(username=username, email=email, password=None)
        user = await user_dao.add(user_data)

    set_tokens(response, user.id)

    return {
        "message": "Успешный вход",
        "user": {"email": email, "username": username},
    }
