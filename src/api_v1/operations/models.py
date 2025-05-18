from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.base import Base
from src.api_v1.operations.schemas import OperationType

if TYPE_CHECKING:
    from src.api_v1.wallets.models import Wallet


class Operation(Base):
    """
    Класс для операции.

    Attributes:
        operation_type (OperationType): Тип операции.
        amount (int): Сумма операции.
        wallet (Wallet): Кошелек, с которым связана операция.
        wallet_id (int): ID кошелька.
    """
    operation_type: Mapped[OperationType]
    amount: Mapped[int]

    wallet: Mapped["Wallet"] = relationship(back_populates="operations")
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id"))

    def to_dict(self):
        """
        Преобразует операцию в словарь.

        Returns:
            Словарь, представляющий операцию.
        """
        return {
            "wallet_id": self.wallet_id,
            "operation_type": self.operation_type,
            "amount": self.amount,
        }
