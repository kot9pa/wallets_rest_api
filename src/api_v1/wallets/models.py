from typing import TYPE_CHECKING, List
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.base import Base

if TYPE_CHECKING:
    from src.api_v1.operations.models import Operation


class Wallet(Base):
    """
    Класс для кошелька.

    Attributes:
        wallet_uuid (str): UUID кошелька.
        balance (int): Баланс кошелька.
        operations (List[Operation]): Список операций, связанных с кошельком.
    """
    wallet_uuid: Mapped[str] = mapped_column(unique=True)
    balance: Mapped[int] = mapped_column(default=0)

    operations: Mapped[List["Operation"]] = relationship(
        back_populates="wallet", cascade="all, delete-orphan")

    def to_dict(self):
        """
        Преобразует кошелек в словарь.

        Returns:
            Словарь, представляющий кошелек.
        """
        return {
            "id": self.id,
            "wallet_uuid": self.wallet_uuid,
            "balance": self.balance,
        }
