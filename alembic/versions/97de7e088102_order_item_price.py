"""order item price

Revision ID: 97de7e088102
Revises: b2ffe28b9117
Create Date: 2025-01-05 01:28:03.505839

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97de7e088102'
down_revision: Union[str, None] = 'b2ffe28b9117'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'order_items', sa.Column('price', sa.Float, nullable=False)
    )


def downgrade() -> None:
    op.drop_column('order_items', 'price')
