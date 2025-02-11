"""inventory product fk

Revision ID: 525ff5665c0d
Revises: 65b992f47e74
Create Date: 2025-01-02 13:53:23.781783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '525ff5665c0d'
down_revision: Union[str, None] = '65b992f47e74'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        'product_inventory_fk',
        'inventory',
        'products',
        ['product_id'],
        ['id'],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_inventory_fk', 'inventory')
    # ### end Alembic commands ###
