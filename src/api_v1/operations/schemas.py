from enum import Enum
from pydantic import BaseModel


class OperationType(str, Enum):
    """
    Тип операции.

    Attributes:
        DEPOSIT (str): Пополнение.
        WITHDRAW (str): Снятие.
    """
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"


class OperationBase(BaseModel):
    """
    Базовый класс для операции.

    Attributes:
        operation_type (OperationType): Тип операции.
        amount (int): Сумма операции.
    """
    operation_type: OperationType
    amount: int


class OperationCreate(OperationBase):
    """
    Класс для создания операции.

    Attributes:
        wallet_id (int): ID кошелька.
    """
    wallet_id: int
