from datetime import date
from pydantic import BaseModel, Field


class SMessageBase(BaseModel):
    sender_id: int = Field(..., description="ID отправителя")
    chat_id: int = Field(..., description="ID чата")
    content: str = Field(..., description="Содержимое сообщения")


class SMessageCreate(SMessageBase):
    pass


class SMessageRead(SMessageBase):
    id: int = Field(..., description="ID сообщения")
    created_at: date = Field(..., description="Дата создания")

    class Config:
        from_attributes = True


class SChatBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название чата")
    owner_id: int = Field(..., description="ID владельца")


class SChatCreate(SChatBase):
    pass


class SChatRead(SChatBase):
    id: int = Field(..., description="ID чата")
    name: str = Field(..., min_length=1, max_length=100, description="Название чата")
    created_at: date = Field(..., description="Дата создания")

    class Config:
        from_attributes = True


class SChatMemberBase(BaseModel):
    chat_id: int = Field(..., description="ID чата")
    user_id: int = Field(..., description="ID пользователя")


class SChatMemberCreate(SChatMemberBase):
    pass


class SChatMemberRead(SChatMemberBase):
    id: int = Field(..., description="ID участника")

    class Config:
        from_attributes = True
