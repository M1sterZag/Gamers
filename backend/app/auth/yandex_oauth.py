from fastapi import APIRouter, Response, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from starlette.responses import RedirectResponse

from app.auth.dao import UsersDAO
from app.auth.utils import set_tokens
from app.dao.dependencies import get_session_with_commit
from app.config import settings

router = APIRouter()


@router.get("/yandex/callback")
async def yandex_code(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_session_with_commit)
):
    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code")

    async with httpx.AsyncClient() as client:
        token_resp = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": settings.yandex.CLIENT_ID,
                "client_secret": settings.yandex.CLIENT_SECRET
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        token_data = token_resp.json()

        if 'access_token' not in token_data:
            raise HTTPException(status_code=400, detail="Invalid code or Yandex error")

        access_token = token_data['access_token']
        user_info = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"}
        )

        if user_info.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail="Не удалось получить информацию о пользователе"
            )

        info = user_info.json()
        email = info.get("default_email")
        username = info.get("login")
        avatar_id = info.get("default_avatar_id")
        yandex_id = info.get("id")
        avatar_url = f"https://avatars.yandex.net/get-yapic/{avatar_id}/islands-200" if avatar_id else None

        user = await UsersDAO.find_one_or_none(session, email=email)
        if not user:
            user_data = {
                "username": username,
                "email": email,
                "yandex_id": yandex_id,
                "password": None,
                "avatar": avatar_url
            }
            user = await UsersDAO.add(session=session, **user_data)

        redirect = RedirectResponse(url="https://gamers-team.ru")
        set_tokens(redirect, user.id)
        return redirect
