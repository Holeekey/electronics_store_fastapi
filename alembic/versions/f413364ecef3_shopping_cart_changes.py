"""shopping cart changes

Revision ID: f413364ecef3
Revises: 525ff5665c0d
Create Date: 2025-01-03 13:35:12.610577

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f413364ecef3'
down_revision: Union[str, None] = '525ff5665c0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table('shopping_cart')
    op.create_table(
        'shopping_cart',
        sa.Column('id', sa.UUID, primary_key=True),
        sa.Column('user_id', sa.String, nullable=False),
    )
    op.create_foreign_key(
        'user_shopping_cart_fk',
        'shopping_cart',
        'users',
        ['user_id'],
        ['id'],
    )
    op.create_table(
        'shopping_cart_items',
        sa.Column('shopping_cart_id', sa.UUID, nullable=False),
        sa.Column('product_id', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('created_at',sa.DateTime, nullable=False),
        sa.Column('updated_at',sa.DateTime, nullable=True),
    )
    op.create_foreign_key(
        'product_shopping_cart_item_fk',
        'shopping_cart_items',
        'products',
        ['product_id'],
        ['id'],
    )
    op.create_foreign_key(
        'shopping_cart_shopping_cart_item_fk',
        'shopping_cart_items',
        'shopping_cart',
        ['shopping_cart_id'],
        ['id'],
    )
    op.create_primary_key(
        'shopping_cart_item_pk',
        'shopping_cart_items',
        ['product_id','shopping_cart_id'],
    )


def downgrade() -> None:
    op.drop_table('shopping_cart_items')
    op.drop_table('shopping_cart')
    op.create_table(
        'shopping_cart',
        sa.Column('product_id', sa.String, nullable=False),
        sa.Column('user_id', sa.String, nullable=False),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('created_at',sa.DateTime, nullable=False),
        sa.Column('updated_at',sa.DateTime, nullable=True),
    )
    op.create_foreign_key(
        'product_shopping_cart_fk',
        'shopping_cart',
        'products',
        ['product_id'],
        ['id'],
    )
    op.create_foreign_key(
        'user_shopping_cart_fk',
        'shopping_cart',
        'users',
        ['user_id'],
        ['id'],
    )
    op.create_primary_key(
        'shopping_cart_pk',
        'shopping_cart',
        ['product_id','user_id'],
    )
