from typing import List, TypeVar, Generic, Type

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base
from app.dao.database import async_session_maker
from .dependencies import get_session_with_commit, get_session_without_commit


class BaseDAO:
    model = None

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            data_id: Критерии фильтрации в виде идентификатора записи.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """

        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        """
        Асинхронно находит и возвращает один экземпляр модели по указанным критериям или None.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Экземпляр модели или None, если ничего не найдено.
        """
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        """
        Асинхронно находит и возвращает все экземпляры модели, удовлетворяющие указанным критериям.

        Аргументы:
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Список экземпляров модели.
        """
        query = select(cls.model).filter_by(**filter_by)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        """
        Асинхронно создает новый экземпляр модели с указанными значениями.

        Аргументы:
            **values: Именованные параметры для создания нового экземпляра модели.

        Возвращает:
            Созданный экземпляр модели.
        """
        new_instance = cls.model(**values)
        session.add(new_instance)

    @classmethod
    async def add_many(cls, instances: list[dict], session: AsyncSession):
        """
        Асинхронно создает несколько новых экземпляров модели с указанными значениями.

        Аргументы:
            instances: Список словарей, где каждый словарь содержит именованные параметры для создания нового
            экземпляра модели.

        Возвращает:
            Список созданных экземпляров модели.
        """
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)

    @classmethod
    async def update(cls, filter_by, session: AsyncSession, **values):
        """
        Асинхронно обновляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by,
        новыми значениями, указанными в values.

        Аргументы:
            filter_by: Критерии фильтрации в виде именованных параметров.
            **values: Именованные параметры для обновления значений экземпляров модели.

        Возвращает:
            Количество обновленных экземпляров модели.
        """
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        result = await session.execute(query)
        return result.rowcount

    @classmethod
    async def delete(cls, session: AsyncSession, delete_all: bool = False, **filter_by):
        """
        Асинхронно удаляет экземпляры модели, удовлетворяющие критериям фильтрации, указанным в filter_by.

        Аргументы:
            delete_all: Если True, удаляет все экземпляры модели без фильтрации.
            **filter_by: Критерии фильтрации в виде именованных параметров.

        Возвращает:
            Количество удаленных экземпляров модели.
        """
        if not delete_all and not filter_by:
            raise ValueError("Необходимо указать хотя бы один параметр для удаления или установить delete_all=True.")

        query = sqlalchemy_delete(cls.model)
        if not delete_all:
            query = query.filter_by(**filter_by)

        result = await session.execute(query)
        return result.rowcount

# T = TypeVar("T", bound=Base)


# class BaseDAO(Generic[T]):
#     model: Type[T] = None
#
#     def __init__(self, session: AsyncSession):
#         self._session = session
#         if self.model is None:
#             raise ValueError("Модель должна быть указана в дочернем классе")
#
#     async def find_one_or_none_by_id(self, data_id: int):
#         try:
#             query = select(self.model).filter_by(id=data_id)
#             result = await self._session.execute(query)
#             record = result.scalar_one_or_none()
#             log_message = f"Запись {self.model.__name__} с ID {data_id} {'найдена' if record else 'не найдена'}."
#             logger.info(log_message)
#             return record
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
#             raise
#
#     async def find_one_or_none(self, filters: BaseModel):
#         filter_dict = filters.model_dump(exclude_unset=True)
#         logger.info(f"Поиск одной записи {self.model.__name__} по фильтрам: {filter_dict}")
#         try:
#             query = select(self.model).filter_by(**filter_dict)
#             result = await self._session.execute(query)
#             record = result.scalar_one_or_none()
#             log_message = f"Запись {'найдена' if record else 'не найдена'} по фильтрам: {filter_dict}"
#             logger.info(log_message)
#             return record
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при поиске записи по фильтрам {filter_dict}: {e}")
#             raise
#
#     async def find_all(self, filters: BaseModel | None = None):
#         filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
#         logger.info(f"Поиск всех записей {self.model.__name__} по фильтрам: {filter_dict}")
#         try:
#             query = select(self.model).filter_by(**filter_dict)
#             result = await self._session.execute(query)
#             records = result.scalars().all()
#             logger.info(f"Найдено {len(records)} записей.")
#             return records
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_dict}: {e}")
#             raise
#
#     async def add(self, values: BaseModel):
#         values_dict = values.model_dump(exclude_unset=True)
#         logger.info(f"Добавление записи {self.model.__name__} с параметрами: {values_dict}")
#         try:
#             new_instance = self.model(**values_dict)
#             self._session.add(new_instance)
#             logger.info(f"Запись {self.model.__name__} успешно добавлена.")
#             await self._session.flush()
#             return new_instance
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при добавлении записи: {e}")
#             raise
#
#     async def add_many(self, instances: List[BaseModel]):
#         values_list = [item.model_dump(exclude_unset=True) for item in instances]
#         logger.info(f"Добавление нескольких записей {self.model.__name__}. Количество: {len(values_list)}")
#         try:
#             new_instances = [self.model(**values) for values in values_list]
#             self._session.add_all(new_instances)
#             logger.info(f"Успешно добавлено {len(new_instances)} записей.")
#             await self._session.flush()
#             return new_instances
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при добавлении нескольких записей: {e}")
#             raise
#
#     async def update(self, filters: BaseModel, values: BaseModel):
#         filter_dict = filters.model_dump(exclude_unset=True)
#         values_dict = values.model_dump(exclude_unset=True)
#         logger.info(
#             f"Обновление записей {self.model.__name__} по фильтру: {filter_dict} с параметрами: {values_dict}")
#         try:
#             query = (
#                 sqlalchemy_update(self.model)
#                 .where(*[getattr(self.model, k) == v for k, v in filter_dict.items()])
#                 .values(**values_dict)
#                 .execution_options(synchronize_session="fetch")
#             )
#             result = await self._session.execute(query)
#             logger.info(f"Обновлено {result.rowcount} записей.")
#             await self._session.flush()
#             return result.rowcount
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при обновлении записей: {e}")
#             raise
#
#     async def delete(self, filters: BaseModel):
#         filter_dict = filters.model_dump(exclude_unset=True)
#         logger.info(f"Удаление записей {self.model.__name__} по фильтру: {filter_dict}")
#         if not filter_dict:
#             logger.error("Нужен хотя бы один фильтр для удаления.")
#             raise ValueError("Нужен хотя бы один фильтр для удаления.")
#         try:
#             query = sqlalchemy_delete(self.model).filter_by(**filter_dict)
#             result = await self._session.execute(query)
#             logger.info(f"Удалено {result.rowcount} записей.")
#             await self._session.flush()
#             return result.rowcount
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при удалении записей: {e}")
#             raise
#
#     async def count(self, filters: BaseModel | None = None):
#         filter_dict = filters.model_dump(exclude_unset=True) if filters else {}
#         logger.info(f"Подсчет количества записей {self.model.__name__} по фильтру: {filter_dict}")
#         try:
#             query = select(func.count(self.model.id)).filter_by(**filter_dict)
#             result = await self._session.execute(query)
#             count = result.scalar()
#             logger.info(f"Найдено {count} записей.")
#             return count
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при подсчете записей: {e}")
#             raise
#
#     async def bulk_update(self, records: List[BaseModel]):
#         logger.info(f"Массовое обновление записей {self.model.__name__}")
#         try:
#             updated_count = 0
#             for record in records:
#                 record_dict = record.model_dump(exclude_unset=True)
#                 if 'id' not in record_dict:
#                     continue
#
#                 update_data = {k: v for k, v in record_dict.items() if k != 'id'}
#                 stmt = (
#                     sqlalchemy_update(self.model)
#                     .filter_by(id=record_dict['id'])
#                     .values(**update_data)
#                 )
#                 result = await self._session.execute(stmt)
#                 updated_count += result.rowcount
#
#             logger.info(f"Обновлено {updated_count} записей")
#             await self._session.flush()
#             return updated_count
#         except SQLAlchemyError as e:
#             logger.error(f"Ошибка при массовом обновлении: {e}")
#             raise
