from pydantic import ConfigDict, model_validator
from app.auth.utils import get_password_hash

from pydantic import BaseModel, EmailStr, Field
from datetime import date


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SUserRegister(User):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=255, description="Пароль, от 8 до 255 знаков")
    confirm_password: str = Field(..., min_length=8, max_length=255, description="Пароль, от 8 до 255 знаков")
    username: str = Field(..., min_length=3, max_length=60, description="Имя, от 3 до 60 символов")

    @model_validator(mode="after")
    def check_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)
        return self


class SUserAuth(User):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=60, description="Пароль, от 8 до 60 знаков")


class SUserRead(User):
    id: int = Field(..., description="Идентификатор пользователя")
    email: EmailStr = Field(..., description="Электронная почта")
    username: str = Field(..., min_length=3, max_length=60, description="Имя, от 3 до 60 символов")
    avatar: str | None = None
    is_active: bool = Field(..., description="Отстранение пользователя")
    is_admin: bool = Field(..., description="Права пользователя")
    created_at: date = Field(..., description="Дата создания аккаунта")


class SUserUpdate(BaseModel):
    username: str = Field(None, min_length=3, max_length=60)
    email: EmailStr = Field(None)
    avatar: str | None = Field(None)
    is_active: bool = Field(None)
    is_admin: bool = Field(None)
    model_config = ConfigDict(from_attributes=True)
