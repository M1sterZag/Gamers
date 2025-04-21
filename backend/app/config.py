import os

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class DBSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    @property
    def db_url(self) -> str:
        # postgresql+asyncpg://postgres:postgres@localhost:5432/db
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="allow")


class AuthJWT(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="allow")


class GoogleAuth(BaseSettings):
    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="allow")


class AppSettings(BaseSettings):
    app_secret_key: str

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="allow")


class Settings(BaseSettings):
    BASE_DIR: str = BASE_DIR
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()
    google_auth: GoogleAuth = GoogleAuth()
    app_settings: AppSettings = AppSettings()

    model_config = SettingsConfigDict(extra="allow")


logger.info("Формируем окружение переменных (settings)")
settings = Settings()
