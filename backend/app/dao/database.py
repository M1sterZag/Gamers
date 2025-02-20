from datetime import datetime
from sqlalchemy import func, TIMESTAMP, Integer, inspect
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, declared_attr
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from app.config import settings

engine = create_async_engine(url=settings.db.db_url)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now()
    )
