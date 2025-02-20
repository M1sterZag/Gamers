from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi import FastAPI, APIRouter, Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

from app.auth.router import router as router_auth
from app.config import settings
from app.exceptions import TokenExpiredException, TokenNoFoundException
from fastapi.exceptions import HTTPException

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


# @app.get("/")
# async def redirect_to_auth():
#     return RedirectResponse(url="/auth")

@app.get("/")
async def hello():
    return {"message": "ok"}

# @app.exception_handler(TokenExpiredException)
# async def token_expired_exception_handler(request: Request, exc: HTTPException):
#     # Возвращаем редирект на страницу /auth
#     return RedirectResponse(url="/auth")
#
#
# @app.exception_handler(TokenNoFoundException)
# async def token_no_found_exception_handler(request: Request, exc: HTTPException):
#     # Возвращаем редирект на страницу /auth
#     return RedirectResponse(url="/auth")

# @asynccontextmanager
# async def lifespan(app: FastAPI) -> AsyncGenerator[dict, None]:
#     """Управление жизненным циклом приложения."""
#     logger.info("Инициализация приложения...")
#     yield
#     logger.info("Завершение работы приложения...")


# def create_app() -> FastAPI:
#     """
#    Создание и конфигурация FastAPI приложения.
#
#    Returns:
#        Сконфигурированное приложение FastAPI
#    """
#     app = FastAPI(
#         lifespan=lifespan,
#     )
#
#     # Настройка CORS
#     app.add_middleware(
#         CORSMiddleware,
#         allow_origins=["*"],
#         allow_credentials=True,
#         allow_methods=["*"],
#         allow_headers=["*"]
#     )
#
#     app.add_middleware(SessionMiddleware, secret_key=settings.app_settings.app_secret_key)
#
#     # Регистрация роутеров
#     register_routers(app)
#
#     return app
#
#
# def register_routers(app: FastAPI) -> None:
#     """Регистрация роутеров приложения."""
#     # Корневой роутер
#     root_router = APIRouter()
#
#     @root_router.get("/", tags=["root"])
#     def home_page():
#         return {
#             "message": "ok"
#         }

# Подключение роутеров
#     app.include_router(root_router, tags=["root"])
#     app.include_router(router_auth, prefix='/auth', tags=['Auth'])
#
#
# # Создание экземпляра приложения
# app = create_app()
