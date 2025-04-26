from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.subscription.dao import SubscriptionDAO, UserSubscriptionDAO

router = APIRouter()


@router.get("")
async def get_subscriptions(session: AsyncSession = Depends(get_session_without_commit)):
    return await SubscriptionDAO.find_all(session=session)


@router.post("/subscribe/{sub_id}")
async def subscribe(
        sub_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    # Находим подписку по ID
    subscription = await SubscriptionDAO.find_one_or_none_by_id(session=session, data_id=sub_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    # Создаем запись о подписке пользователя
    end_date = datetime.now() + subscription.duration
    await UserSubscriptionDAO.add(
        session=session,
        user_id=current_user.id,
        subscription_id=subscription.id,
        end_date=end_date,
    )

    return {"message": "Подписка успешно оформлена"}


@router.post("/check_subscription")
async def check_subscription(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_without_commit)
):
    # Проверяем активную подписку
    subscription = await UserSubscriptionDAO.find_one_or_none(
        session=session,
        user_id=current_user.id,
        is_active=True,
        end_date__gt=datetime.now(),
    )
    if not subscription:
        raise HTTPException(status_code=403, detail="У вас нет активной подписки")
    return subscription
