from typing import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.database import async_session_maker


async def get_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия с автоматическим коммитом."""
    async with async_session_maker() as session:
        try:
            logger.info("Получение асинхронной сессии с коммитом")
            yield session
            logger.info("Фиксация изменений в асинхронной сессии с коммитом")
            await session.commit()
        except Exception:
            logger.info("Откат изменений асинхронной сессии с коммитом")
            await session.rollback()
            raise
        finally:
            logger.info("Закрытие асинхронной сессии с коммитом")
            await session.close()


async def get_session_without_commit() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронная сессия без автоматического коммита."""
    async with async_session_maker() as session:
        try:
            logger.info("Получение асинхронной сессии без коммита")
            yield session
        except Exception:
            logger.info("Откат изменений асинхронной сессии без коммита")
            await session.rollback()
            raise
        finally:
            logger.info("Закрытие асинхронной сессии без коммита")
            await session.close()
