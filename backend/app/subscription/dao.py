from app.dao.base import BaseDAO
from app.subscription.models import Subscription, UserSubscription


class SubscriptionDAO(BaseDAO):
    model = Subscription


class UserSubscriptionDAO(BaseDAO):
    model = UserSubscription
