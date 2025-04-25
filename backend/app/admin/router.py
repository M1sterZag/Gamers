from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
import json
from app.admin.dao import find_all_by_table_name_with_limit, TABLE_MODEL_MAPPING
from app.auth.dependencies import get_current_admin_user
from app.auth.models import User
from app.dao.dependencies import get_session_with_commit

router = APIRouter()


@router.get("/tables")
async def get_tables(current_admin: User = Depends(get_current_admin_user)):
    return {"tables": list(TABLE_MODEL_MAPPING.keys())}


@router.get("/table/{table_name}")
async def get_table_data(
        table_name: str,
        limit: int = 10,
        session: AsyncSession = Depends(get_session_with_commit),
        current_admin: User = Depends(get_current_admin_user)
):
    """
    Получает данные из указанной таблицы с заданным лимитом, смещением и фильтрами.

    Аргументы:
        table_name: Имя таблицы (например, 'users', 'messages').
        limit: Максимальное количество записей для возврата (по умолчанию 10).
        session: Асинхронная сессия SQLAlchemy.
        current_admin: Текущий администратор.

    Возвращает:
        Словарь с ключами 'columns' (список имён столбцов) и 'data' (список записей).

    Raises:
        HTTPException: Если таблица не найдена, лимит некорректен или произошла ошибка.
    """
    try:
        records = await find_all_by_table_name_with_limit(
            session=session,
            table_name=table_name,
            limit=limit,
        )

        # Получаем имена столбцов из модели
        model = TABLE_MODEL_MAPPING.get(table_name)
        if not model:
            raise ValueError(f"Таблица '{table_name}' не найдена в маппинге моделей.")
        columns = list(model.__table__.columns.keys())

        # Преобразуем записи в словари
        data = [
            {column: getattr(record, column) for column in columns}
            for record in records
        ]

        # Возвращаем данные в формате { columns: [], data: [] }
        return {
            "columns": columns,
            "data": data
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Некорректный формат фильтров")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка сервера: {str(e)}")


@router.post("/table/{table_name}")
async def create_record(
        table_name: str,
        record_data: dict,
        session: AsyncSession = Depends(get_session_with_commit),
        current_admin: User = Depends(get_current_admin_user)
):
    if table_name not in TABLE_MODEL_MAPPING:
        raise HTTPException(status_code=404, detail="Table not found")

    model = TABLE_MODEL_MAPPING[table_name]
    stmt = insert(model).values(**record_data)
    await session.execute(stmt)

    return {"status": "success", "message": "Record created"}


@router.put("/table/{table_name}/{record_id}")
async def update_record(
        table_name: str,
        record_id: int,
        record_data: dict,
        session: AsyncSession = Depends(get_session_with_commit),
        current_admin: User = Depends(get_current_admin_user)
):
    if table_name not in TABLE_MODEL_MAPPING:
        raise HTTPException(status_code=404, detail="Table not found")

    model = TABLE_MODEL_MAPPING[table_name]
    stmt = update(model).where(model.id == record_id).values(**record_data)
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"status": "success", "message": "Record updated"}


@router.delete("/table/{table_name}/{record_id}")
async def delete_record(
        table_name: str,
        record_id: int,
        session: AsyncSession = Depends(get_session_with_commit),
        current_admin: User = Depends(get_current_admin_user)
):
    if table_name not in TABLE_MODEL_MAPPING:
        raise HTTPException(status_code=404, detail="Table not found")

    model = TABLE_MODEL_MAPPING[table_name]
    stmt = delete(model).where(model.id == record_id)
    result = await session.execute(stmt)

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Record not found")

    return {"status": "success", "message": "Record deleted"}
