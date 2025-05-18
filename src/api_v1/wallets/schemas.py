from pydantic import BaseModel, ConfigDict, Field


class WalletBase(BaseModel):
    """
    Базовый класс для кошелька.

    Attributes:
        wallet_uuid (str): UUID кошелька.
        balance (int): Баланс кошелька.
    """
    model_config = ConfigDict(from_attributes=True)
    wallet_uuid: str
    balance: int = Field(default=0)


class Wallet(WalletBase):
    """
    Attributes:
        id (int): ID кошелька.
    """
    id: int


class WalletView(WalletBase):
    pass
