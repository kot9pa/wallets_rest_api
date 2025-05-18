from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.api_v1.operations.models import Operation
from src.api_v1.operations.schemas import OperationCreate


async def create_operation(session: AsyncSession, operation: OperationCreate) -> Operation:
    """
    Создает операцию.

    Args:
        session (AsyncSession): Сессия базы данных.
        operation (OperationCreate): Операция.

    Returns:
        Созданная операция.

    Raises:
        SQLAlchemyError: Если возникает ошибка базы данных.
    """
    instance = Operation(**operation.model_dump(exclude_none=True))
    session.add(instance)
    try:
        await session.commit()
        return instance
    except SQLAlchemyError as err:
        await session.rollback()
        raise err
