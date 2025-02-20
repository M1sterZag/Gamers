from pydantic import BaseModel, Field
from typing import Optional


class SGameBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название игры")
    avatar: Optional[str] = Field(None, description="Аватар игры")


class SGameCreate(SGameBase):
    pass


class SGameRead(SGameBase):
    id: int = Field(..., description="ID игры")

    class Config:
        from_attributes = True


class SGameTypeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Тип игры")


class SGameTypeCreate(SGameTypeBase):
    pass


class SGameTypeRead(SGameTypeBase):
    id: int = Field(..., description="ID типа игры")

    class Config:
        from_attributes = True
