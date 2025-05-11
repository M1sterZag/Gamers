import os
from pathlib import Path
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class BaseEnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/../.env", extra="allow")


class DBSettings(BaseEnvSettings):
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_NAME: str
    DB_PASS: str

    @property
    def db_url(self) -> str:
        # postgresql+asyncpg://postgres:postgres@localhost:5432/db
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class AuthJWT(BaseEnvSettings):
    SECRET_KEY: str
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    private_key_path: Path = Path(BASE_DIR) / "certs" / "jwt-private.pem"
    public_key_path: Path = Path(BASE_DIR) / "certs" / "jwt-public.pem"

    @property
    def private_key(self) -> str:
        return Path(self.private_key_path).read_text()

    @property
    def public_key(self) -> str:
        return Path(self.public_key_path).read_text()


class UKassa(BaseEnvSettings):
    UKASSA_KEY: str
    UKASSA_SHOP_ID: str


class YandexOAuthSettings(BaseEnvSettings):
    YANDEX_CLIENT_ID: str
    YANDEX_CLIENT_SECRET: str


class AppSettings(BaseEnvSettings):
    app_secret_key: str


class Settings(BaseSettings):
    BASE_DIR: str = BASE_DIR
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()
    ukassa: UKassa = UKassa()
    yandex: YandexOAuthSettings = YandexOAuthSettings()
    app_settings: AppSettings = AppSettings()

    model_config = SettingsConfigDict(extra="allow")


logger.info("Формируем окружение переменных (settings)")
settings = Settings()
