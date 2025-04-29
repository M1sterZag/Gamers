from pydantic import BaseModel, Field, ConfigDict


class SSubscriptionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название подписки")
    price: float = Field(..., gt=0, description="Цена подписки")
    duration: int = Field(..., gt=0, description="Продолжительность подписки в днях")

    model_config = ConfigDict(from_attributes=True)


class SSubscriptionCreate(SSubscriptionBase):
    pass


class SSubscriptionRead(SSubscriptionBase):
    id: int = Field(..., description="ID подписки")

    class Config:
        from_attributes = True
