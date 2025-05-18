from typing import Annotated
from fastapi import HTTPException, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.wallets import orm
from src.api_v1.wallets.models import Wallet
from src.database import db_helper


async def get_wallet_by_uuid(
    wallet_uuid: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
) -> Wallet:
    """
    Получает кошелек по UUID.

    Args:
        wallet_uuid (str): UUID кошелька.
        session (AsyncSession): Сессия базы данных.

    Returns:
        Кошелек, если он существует.

    Raises:
        HTTPException: Если кошелек не найден.
    """
    result = await orm.get_wallet(session=session, wallet_uuid=wallet_uuid)
    if result is not None:
        return result

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Wallet [{wallet_uuid=}] not found",
    )
