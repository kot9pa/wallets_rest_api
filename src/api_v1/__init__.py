from fastapi import APIRouter
from src.api_v1.wallets.views import router as wallets_router
from src.api_v1.wallets.models import Wallet
from src.api_v1.operations.models import Operation

__all__ = (
    "Wallet",
    "Operation",
)

api_router = APIRouter()
api_router.include_router(router=wallets_router)
