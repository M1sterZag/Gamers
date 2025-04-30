from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.chat.models import Message, Chat, ChatMember
from app.game.models import Game, GameType
from app.subscription.models import Subscription, UserSubscription
from app.team.models import Team, TeamMember

TABLE_MODEL_MAPPING = {
    "users": User,
    "messages": Message,
    "chats": Chat,
    "chat_members": ChatMember,
    "games": Game,
    "game_types": GameType,
    "teams": Team,
    "team_members": TeamMember,
    "subscriptions": Subscription,
    "user_subscriptions": UserSubscription
}


async def find_all_by_table_name_with_limit(
        session: AsyncSession, table_name: str, limit: int
):
    """
    Асинхронно находит и возвращает записи из указанной таблицы с заданным лимитом.

    Аргументы:
        session: Асинхронная сессия SQLAlchemy.
        table_name: Имя таблицы (например, 'users', 'messages').
        limit: Максимальное количество записей для возврата.

    Возвращает:
        Список экземпляров модели, ограниченный указанным лимитом.

    Raises:
        ValueError: Если table_name не соответствует ни одной модели или limit меньше или равен 0.
    """
    if limit <= 0:
        raise ValueError("Лимит должен быть положительным числом.")

    model = TABLE_MODEL_MAPPING.get(table_name)
    if not model:
        raise ValueError(f"Таблица '{table_name}' не найдена в маппинге моделей.")

    logger.info(
        "Ищем записи в базе с лимитом: таблица={}, лимит={}",
        table_name,
        limit
    )
    query = select(model).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()
