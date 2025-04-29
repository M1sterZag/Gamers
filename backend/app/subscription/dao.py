from datetime import datetime

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.subscription.models import Subscription, UserSubscription


class SubscriptionDAO(BaseDAO):
    model = Subscription


class UserSubscriptionDAO(BaseDAO):
    model = UserSubscription

    @classmethod
    async def find_active_subscription(
            cls, session: AsyncSession, user_id: int
    ):
        query = select(cls.model).filter(
            and_(
                cls.model.user_id == user_id,
                cls.model.is_active == True,
                cls.model.end_date > datetime.now()
            )
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
