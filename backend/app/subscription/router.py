from datetime import datetime, timedelta

import requests
from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user, get_current_admin_user
from app.auth.models import User
from app.dao.dependencies import get_session_with_commit, get_session_without_commit
from app.subscription.dao import SubscriptionDAO, UserSubscriptionDAO
from app.subscription.schemas import SSubscriptionCreate
from app.config import settings

from yookassa import Payment, Configuration
import uuid

router = APIRouter()

Configuration.account_id = settings.ukassa.UKASSA_SHOP_ID
Configuration.secret_key = settings.ukassa.UKASSA_KEY


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


# @router.post("/subscribe/{sub_id}")
# async def subscribe(
#         sub_id: int,
#         payment_data: dict,
#         current_user: User = Depends(get_current_user),
#         session: AsyncSession = Depends(get_session_with_commit)
# ):
#     subscription = await SubscriptionDAO.find_one_or_none_by_id(session=session, data_id=sub_id)
#     if not subscription:
#         raise HTTPException(status_code=404, detail="Подписка не найдена")
#
#     # Создаем запись о подписке пользователя
#     start_date = datetime.now()
#     end_date = start_date + timedelta(days=subscription.duration)
#     await UserSubscriptionDAO.add(
#         session=session,
#         user_id=current_user.id,
#         subscription_id=subscription.id,
#         start_date=start_date,
#         end_date=end_date,
#     )
#
#     return {"message": "Подписка успешно оформлена"}


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


@router.post("/create_payment/{sub_id}")
async def create_payment(
        sub_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_session_with_commit)
):
    """
    Создает платеж в ЮKassa и возвращает ссылку для оплаты.
    """
    logger.info(f"Пытаюсь найти подписку {sub_id}")
    subscription = await SubscriptionDAO.find_one_or_none_by_id(session=session, data_id=sub_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Подписка не найдена")

    # Генерация уникального idempotence_key
    idempotence_key = str(uuid.uuid4())

    # Формируем данные для создания платежа
    payment_data = {
        "amount": {
            "value": "{:.2f}".format(float(subscription.price)),
            "currency": "RUB",
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://gamers-team.ru/premium",
        },
        "description": f"Оплата подписки {subscription.name}",
        "capture": True,
    }

    logger.info(f"Отправляемые данные в ЮKassa: {payment_data}")

    try:
        # Создаем платеж через библиотеку YooKassa
        payment = Payment.create(payment_data, idempotence_key)

        # Получаем ссылку для подтверждения оплаты
        confirmation_url = payment.confirmation.confirmation_url

        # Сохраняем ID платежа для дальнейшей проверки
        await UserSubscriptionDAO.add(
            session=session,
            user_id=current_user.id,
            subscription_id=sub_id,
            payment_id=payment.id,
            is_active=False,
            start_date=datetime.now(),
            end_date=datetime.now(),
        )

        logger.info(f"Ссылка для подтверждения оплаты: {confirmation_url}")
        return {"confirmation_url": confirmation_url}

    except Exception as e:
        logger.error(f"Ошибка при создании платежа: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при создании платежа")


@router.post("/yookassa_webhook")
async def yookassa_webhook(request: Request, session: AsyncSession = Depends(get_session_with_commit)):
    """
    Обрабатывает уведомление от ЮKassa о статусе платежа.
    """
    try:
        data = await request.json()
        event = data.get("event")
        payment = data.get("object")

        logger.info(f"Проверяем ответный платеж {payment['id']}")
        if event == "payment.succeeded":
            # Проверяем, что платеж успешно завершен
            payment_id = payment["id"]
            user_subscription = await UserSubscriptionDAO.find_one_or_none(
                session=session,
                payment_id=payment_id
            )

            if user_subscription:
                # Рассчитываем даты начала и окончания подписки
                start_date = datetime.now()
                subscription = await SubscriptionDAO.find_one_or_none_by_id(
                    session=session,
                    data_id=user_subscription.subscription_id
                )
                if not subscription:
                    raise HTTPException(status_code=404, detail="Подписка не найдена")

                end_date = start_date + timedelta(days=subscription.duration)

                # Обновляем запись о подписке
                logger.info(f"Обновляем оплаченную подписку")
                updated_count = await UserSubscriptionDAO.update(
                    filter_by={
                        "user_id": user_subscription.user_id,
                        "subscription_id": user_subscription.subscription_id,
                    },
                    session=session,
                    start_date=start_date,
                    end_date=end_date,
                    is_active=True,  # Активируем подписку
                )

                if updated_count > 0:
                    return {"status": "success"}

        return {"status": "ignored"}

    except Exception as e:
        logger.error(f"Ошибка при обработке webhook: {e}")
        raise HTTPException(status_code=500, detail="Ошибка при обработке уведомления от ЮKassa")
