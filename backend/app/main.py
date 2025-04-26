from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.auth.router import router as router_auth
from app.team.router import router as router_teams
from app.game.router import router as router_games
from app.chat.router import router as router_chats
from app.admin.router import router as router_admin
from app.subscription.router import router as router_subscriptions

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost", "http://frontend"],
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


@app.get("/")
async def hello():
    return {"message": "ok"}
