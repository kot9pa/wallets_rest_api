from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.api_v1.wallets.models import Wallet


async def get_wallets(session: AsyncSession) -> list[Wallet] | None:
    """
    Получает все кошельки.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        Список кошельков, если они существуют.

    Raises:
        SQLAlchemyError: Если возникает ошибка базы данных.
    """
    results = await session.scalars(select(Wallet).order_by(Wallet.id))
    values = results.all()
    if not values:
        return
    return values


async def get_wallet(session: AsyncSession, wallet_uuid: str) -> Wallet | None:
    """
    Получает кошелек по UUID.

    Args:
        session (AsyncSession): Сессия базы данных.
        wallet_uuid (str): UUID кошелька.

    Returns:
        Кошелек, если он существует.

    Raises:
        SQLAlchemyError: Если возникает ошибка базы данных.
    """
    stmt = select(Wallet).filter_by(wallet_uuid=wallet_uuid)
    value = await session.scalar(stmt)
    if not value:
        return
    return value


async def deposit_to_wallet(session: AsyncSession, wallet: Wallet, amount: int) -> Wallet:
    """
    Пополняет баланс кошелька.

    Args:
        session (AsyncSession): Сессия базы данных.
        wallet (Wallet): Кошелек.
        amount (int): Сумма пополнения.

    Returns:
        Кошелек с обновленным балансом.

    Raises:
        SQLAlchemyError: Если возникает ошибка базы данных.
    """
    wallet.balance += amount
    session.add(wallet)
    try:
        await session.commit()
        return wallet
    except SQLAlchemyError as err:
        await session.rollback()
        raise err


async def withdraw_from_wallet(session: AsyncSession, wallet: Wallet, amount: int) -> bool:
    """
    Снимает деньги с кошелька.

    Args:
        session (AsyncSession): Сессия базы данных.
        wallet (Wallet): Кошелек.
        amount (int): Сумма снятия.

    Returns:
        Кошелек с обновленным балансом.

    Raises:
        SQLAlchemyError: Если возникает ошибка базы данных.
    """
    wallet.balance -= amount
    session.add(wallet)
    try:
        await session.commit()
        return wallet
    except SQLAlchemyError as err:
        await session.rollback()
        raise err
