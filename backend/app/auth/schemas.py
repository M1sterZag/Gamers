from pydantic import ConfigDict, model_validator
from app.auth.utils import get_password_hash

from pydantic import BaseModel, EmailStr, Field
from datetime import date


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SUserRegister(User):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 знаков")
    confirm_password: str = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 знаков")
    username: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")

    @model_validator(mode="after")
    def check_password(self):
        if self.password != self.confirm_password:
            raise ValueError("Пароли не совпадают")
        self.password = get_password_hash(self.password)
        return self


class SUserAuth(User):
    email: EmailStr = Field(..., description="Электронная почта")
    password: str = Field(..., min_length=8, max_length=50, description="Пароль, от 8 до 50 знаков")


class SUserRead(User):
    id: int = Field(..., description="Идентификатор пользователя")
    username: str = Field(..., min_length=3, max_length=50, description="Имя, от 3 до 50 символов")
    avatar: str | None = None
    is_active: bool = Field(..., description="Отстранение пользователя")
    is_admin: bool = Field(..., description="Права пользователя")
    created_at: date = Field(..., description="Дата создания аккаунта")

# class EmailModel(BaseModel):
#     email: EmailStr = Field(description="Электронная почта")
#     model_config = ConfigDict(from_attributes=True)
#
#
# class UserBase(EmailModel):
#     username: str | None = Field(None, max_length=255, description="Имя пользователя")
#
#
# class SUserRegister(UserBase):
#     password: str = Field(min_length=8, max_length=50, description="Пароль")
#     confirm_password: str = Field(min_length=8, max_length=50, description="Повторите пароль")
#
#     @model_validator(mode="after")
#     def check_password(self):
#         if self.password != self.confirm_password:
#             raise ValueError("Пароли не совпадают")
#         self.password = get_password_hash(self.password)
#         return self
#
#
# class SUserAuth(BaseModel):
#     email: EmailStr
#     password: str
#
#
# class SUserAddDB(UserBase):
#     password: str = Field(min_length=8, description="Пароль в формате HASH-строки")
#
#
# class SUserInfo(UserBase):
#     id: int
#     avatar: str | None = None
#     is_active: bool
#     is_admin: bool
#     created_at: date
