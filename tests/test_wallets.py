import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.api_v1.wallets.orm import get_wallets


pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture(autouse=True)
async def get_test_wallets(db_session: AsyncSession):
    return await get_wallets(db_session)


async def test_get_wallets(client: AsyncClient, get_test_wallets):
    response = await client.get(f"{settings.api_v1_prefix}/wallets/")
    assert response.status_code == 200
    json_data = response.json()
    assert 'detail' not in json_data, json_data['detail']
    assert json_data == [wallet.to_dict() for wallet in get_test_wallets]


async def test_get_wallet(client: AsyncClient, get_test_wallets):
    for wallet in get_test_wallets:
        response = await client.get(f"{settings.api_v1_prefix}/wallets/{wallet.wallet_uuid}")
        assert response.status_code == 200
        json_data = response.json()
        assert 'detail' not in json_data, json_data['detail']
        assert json_data['wallet_uuid'] == wallet.wallet_uuid


async def test_deposit_operation_with_wallet(client: AsyncClient, get_test_wallets):
    deposit_amount = 100
    for wallet in get_test_wallets:
        response = await client.post(
            f"{settings.api_v1_prefix}/wallets/{wallet.wallet_uuid}/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": deposit_amount
            }
        )
        assert response.status_code == 202
        json_data = response.json()
        assert 'detail' not in json_data, json_data['detail']
        assert json_data['wallet'] == {
            "balance": wallet.balance + deposit_amount,
            "wallet_uuid": wallet.wallet_uuid,
            "id": json_data["wallet"]["id"],
        }


async def test_withdraw_operation_with_wallet(client: AsyncClient, get_test_wallets):
    withdraw_amount = 100
    for wallet in get_test_wallets:
        response = await client.post(
            f"{settings.api_v1_prefix}/wallets/{wallet.wallet_uuid}/operation",
            json={
                "operation_type": "WITHDRAW",
                "amount": withdraw_amount
            }
        )
        assert response.status_code == 202
        json_data = response.json()
        assert 'detail' not in json_data, json_data['detail']
        assert json_data['wallet'] == {
            "balance": wallet.balance - withdraw_amount,
            "wallet_uuid": wallet.wallet_uuid,
            "id": json_data["wallet"]["id"],
        }
