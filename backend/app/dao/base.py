from loguru import logger
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete
from sqlalchemy.ext.asyncio import AsyncSession


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
        logger.info("Ищем запись в базе по id: таблица={}, фильтр={}", cls.model.__tablename__, {"id": data_id})
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
        logger.info("Ищем запись в базе: таблица={}, фильтр={}", cls.model.__tablename__, filter_by)
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
        logger.info("Ищем все записи в базе: таблица={}, фильтр={}", cls.model.__tablename__, filter_by)
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
        logger.info("Добавляем запись в базу: таблица={}, данные={}", cls.model.__tablename__, values)
        new_instance = cls.model(**values)
        session.add(new_instance)
        await session.flush()
        return new_instance

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
        logger.info("Добавляем много записей в базу: таблица={}, данные={}", cls.model.__tablename__, instances)
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
        logger.info("Добавляем много записей в базу: таблица={}, фильтры={}, данные={}",
                    cls.model.__tablename__, filter_by, values)
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

        logger.info("Удаление записей из таблицы={}", cls.model.__tablename__)
        query = sqlalchemy_delete(cls.model)
        if not delete_all:
            query = query.filter_by(**filter_by)

        result = await session.execute(query)
        return result.rowcount
