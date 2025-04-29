from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_current_admin_user
from app.auth.models import User
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.subscription.dao import SubscriptionDAO, UserSubscriptionDAO
from app.subscription.schemas import SSubscriptionCreate

router = APIRouter()


@router.get("")
async def get_subscriptions(session: AsyncSession = Depends(get_session_without_commit)):
    return await SubscriptionDAO.find_all(session=session)


@router.post("")
async def create_subscription(
        sub_data: SSubscriptionCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Создает новую подписку.
    """
    new_subscription = await SubscriptionDAO.add(session=session, **sub_data.model_dump())
    return new_subscription


@router.delete("/{sub_id}")
async def delete_subscription(
        sub_id: int,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Удаляет подписку по ID.
    """
    deleted = await SubscriptionDAO.delete(session=session, id=sub_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return {"message": "Подписка успешно удалена"}


@router.put("/{sub_id}")
async def update_subscription(
        sub_id: int,
        sub_data: SSubscriptionCreate,
        admin_user=Depends(get_current_admin_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Обновляет данные существующей подписки.
    """
    updated_count = await SubscriptionDAO.update(
        filter_by={"id": sub_id},
        session=session,
        **sub_data.model_dump()
    )
    if updated_count == 0:
        raise HTTPException(status_code=404, detail="Подписка не найдена")
    return {"message": "Подписка успешно обновлена"}


@router.post("/subscribe/{sub_id}")
async def subscribe(
        sub_id: int,
        payment_data: dict,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    subscription = await SubscriptionDAO.find_one_or_none_by_id(session=session, data_id=sub_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    # Создаем запись о подписке пользователя
    start_date = datetime.now()
    end_date = start_date + timedelta(days=subscription.duration)
    await UserSubscriptionDAO.add(
        session=session,
        user_id=current_user.id,
        subscription_id=subscription.id,
        start_date=start_date,
        end_date=end_date,
    )

    return {"message": "Подписка успешно оформлена"}


@router.get("/check_subscription")
async def check_subscription(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_without_commit),
):
    logger.info(f"Проверка активной подписки для пользователя {current_user.username}")
    subscription = await UserSubscriptionDAO.find_active_subscription(
        session=session, user_id=current_user.id
    )
    if not subscription:
        raise HTTPException(status_code=404, detail="У вас нет активной подписки")
    return subscription


@router.get("/subscribed_user_ids")
async def get_subscribed_user_ids(
        session: AsyncSession = Depends(get_session_without_commit)
):
    """
    Возвращает список ID пользователей с активными подписками
    """
    return await UserSubscriptionDAO.get_all_subscribed_user_ids(session=session)
