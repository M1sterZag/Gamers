from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.auth.router import router as router_auth
from app.team.router import router as router_teams
from app.game.router import router as router_games
from app.chat.router import router as router_chats
from app.admin.router import router as router_admin
from app.subscription.router import router as router_subscriptions
from app.auth.yandex_oauth import router as router_yandex_oauth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Локальная разработка
        "http://localhost",  # Локальный сервер
        "http://frontend",  # Docker-контейнер фронтенда
        "http://77.95.201.26",  # IP-адрес сервера
        "https://gamers-team.ru"  # Новый домен
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(router_auth, prefix='/auth', tags=['Auth'])
app.include_router(router_chats, prefix='/ws/chats', tags=['Chats'])
app.include_router(router_teams, prefix='/teams', tags=['Teams'])
app.include_router(router_games, prefix="/games", tags=["Games"])
app.include_router(router_admin, prefix='/admin', tags=['Admin'])
app.include_router(router_subscriptions, prefix='/subscriptions', tags=['Subscriptions'])
app.include_router(router_yandex_oauth, prefix='/oauth', tags=['Yandex'])


@app.get("/")
async def root():
    return RedirectResponse(url="/docs")
