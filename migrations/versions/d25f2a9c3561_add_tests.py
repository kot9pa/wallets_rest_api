"""add tests

Revision ID: d25f2a9c3561
Revises: d3d6b82063e7
Create Date: 2025-05-13 22:53:05.267539

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.api_v1.operations.schemas import OperationType

# revision identifiers, used by Alembic.
revision: str = 'd25f2a9c3561'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Create an ad-hoc table to use for the insert statement.
wallets_table = sa.table(
    "wallets",
    sa.column("id", sa.Integer),
    sa.column("wallet_uuid", sa.String),
    sa.column("balance", sa.Integer),
)

operations_table = sa.table(
    "operations",
    sa.column("id", sa.Integer),
    sa.column("wallet_id", sa.Integer),
    sa.column("operation_type", sa.Enum(OperationType)),
    sa.column("amount", sa.Integer),
)


def upgrade() -> None:
    """Upgrade schema."""
    op.bulk_insert(
        wallets_table,
        [
            {
                "id": id,
                "wallet_uuid": str(uuid4()),
                "balance": 0
            } for id in range(1, 10)
        ],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("TRUNCATE TABLE operations CASCADE")
    op.execute("TRUNCATE TABLE wallets CASCADE")
