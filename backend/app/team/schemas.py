from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class STeamBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название команды")
    game_id: int = Field(..., description="ID игры")
    description: Optional[str] = Field(None, max_length=255, description="Описание команды")
    max_members: int = Field(..., description="Максимальное количество участников")
    owner_id: int = Field(..., description="ID владельца команды")
    chat_id: int = Field(..., description="ID чата команды")
    game_type_id: int = Field(..., description="ID типа игры")
    time: datetime = Field(..., description="Время игры")


class STeamCreate(STeamBase):
    pass


class STeamRead(STeamBase):
    id: int = Field(..., description="ID команды")
    created_at: datetime = Field(..., description="Дата создания")

    class Config:
        from_attributes = True


class STeamMemberBase(BaseModel):
    team_id: int = Field(..., description="ID команды")
    user_id: int = Field(..., description="ID пользователя")


class STeamMemberCreate(STeamMemberBase):
    pass


class STeamMemberRead(STeamMemberBase):
    id: int = Field(..., description="ID участника команды")
    joined_at: datetime = Field(..., description="Дата вступления")

    class Config:
        from_attributes = True
