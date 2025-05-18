from typing import Annotated, List
from fastapi import APIRouter, Path, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.wallets import orm as orm_wallets
from src.api_v1.operations import orm as orm_operations
from src.api_v1.wallets.schemas import Wallet, WalletView
from src.api_v1.operations.schemas import OperationBase, OperationCreate, OperationType
from src.api_v1.operations.models import Operation
from src.dependencies import get_wallet_by_uuid
from src.database import db_helper


router = APIRouter(prefix="/wallets", tags=["Wallet"])


@router.get("/", response_model_exclude_none=List[WalletView])
async def get_wallets(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    """
    Получает все кошельки.

    Args:
        session (AsyncSession): Сессия базы данных.

    Returns:
        Список кошельков, если они существуют.

    Raises:
        HTTPException: Если кошельки не найдены.
    """
    result = await orm_wallets.get_wallets(session=session)
    if not result:
        return {"detail": "Wallets not found"}
    return result


@router.get("/{wallet_uuid}", response_model_exclude_none=WalletView)
async def get_wallet(
    wallet_uuid: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
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
    result = await orm_wallets.get_wallet(session=session, wallet_uuid=wallet_uuid)
    if not result:
        return {"detail": f"Wallet [{wallet_uuid=}] not found"}
    return result


@router.post("/{wallet_uuid}/operation", status_code=status.HTTP_202_ACCEPTED)
async def perform_operation_with_wallet(
    operation_in: OperationBase,
    wallet: Wallet = Depends(get_wallet_by_uuid),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    """
    Выполняет операцию с кошельком.

    Args:
        operation_in (OperationBase): Операция.
        wallet (Wallet): Кошелек.
        session (AsyncSession): Сессия базы данных.

    Returns:
        Результат операции и кошелек.

    Raises:
        ValueError: Если тип операции недопустим.
    """
    # Create operation
    operation_create = OperationCreate(**operation_in.model_dump(), wallet_id=wallet.id)
    operation: Operation = await orm_operations.create_operation(session=session, operation=operation_create)

    # Perform operation
    match operation.operation_type:
        case OperationType.DEPOSIT:
            wallet = await orm_wallets.deposit_to_wallet(
                session=session,
                wallet=wallet,
                amount=operation.amount
            )
        case OperationType.WITHDRAW:
            wallet = await orm_wallets.withdraw_from_wallet(
                session=session,
                wallet=wallet,
                amount=operation.amount
            )
        case _:
            raise ValueError(f"Invalid operation type {operation.operation_type}")

    return {"operation": operation, "wallet": wallet}
