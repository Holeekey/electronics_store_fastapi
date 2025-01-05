"""order table

Revision ID: b2ffe28b9117
Revises: f413364ecef3
Create Date: 2025-01-04 23:55:31.337320

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from src.order.domain.value_objects.order_status import OrderStatusOptions


# revision identifiers, used by Alembic.
revision: str = 'b2ffe28b9117'
down_revision: Union[str, None] = 'f413364ecef3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    order_status_enum = sa.Enum(OrderStatusOptions, name="order_status")
    order_status_enum.create(op.get_bind(), checkfirst=True)
    op.create_table(
        'orders',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('user_id', sa.String, nullable=False),
        sa.Column('created_at',sa.DateTime, nullable=False),
        sa.Column('updated_at',sa.DateTime, nullable=True),
    )
    op.add_column(
        'orders', sa.Column('status', order_status_enum, nullable=False)
    )
    op.create_foreign_key(
        'user_order_fk',
        'orders',
        'users',
        ['user_id'],
        ['id'],
    )
    op.create_table(
        'order_items',
        sa.Column('id', sa.UUID, primary_key=True, nullable=False),
        sa.Column('order_id', sa.UUID, nullable=False),
        sa.Column('product_id', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
    )
    op.create_foreign_key(
        'product_order_item_fk',
        'order_items',
        'products',
        ['product_id'],
        ['id'],
    )
    op.create_foreign_key(
        'order_order_item_fk',
        'order_items',
        'orders',
        ['order_id'],
        ['id'],
    )

def downgrade() -> None:
    op.drop_table('order_items')
    op.drop_table('orders')
