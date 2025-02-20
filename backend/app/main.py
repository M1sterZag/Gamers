from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from app.auth.router import router as router_auth
from app.exceptions import TokenExpiredException, TokenNoFoundException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# app.add_middleware(SessionMiddleware, secret_key=settings.app_settings.app_secret_key)

app.include_router(router_auth, prefix='/auth', tags=['Auth'])


@app.get("/")
async def hello():
    return {"message": "ok"}
