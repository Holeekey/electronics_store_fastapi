"""updated product data

Revision ID: 268668625fb1
Revises: d0372fa77904
Create Date: 2024-12-26 13:26:41.099306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '268668625fb1'
down_revision: Union[str, None] = 'd0372fa77904'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.create_table(
        'products',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('code', sa.String(20), nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('cost', sa.Float, nullable=False),
        sa.Column('margin', sa.Float, nullable=False),
        sa.Column('price', sa.Float, nullable=False),
        sa.Column('earning', sa.Float, nullable=False),
        sa.Column('status', sa.Integer, nullable=False),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.create_table(
        'products',
        sa.Column('id', sa.String, primary_key=True),
        sa.Column('name', sa.String(20), nullable=False),
        sa.Column('price', sa.Float(2), nullable=False),
    )
    # ### end Alembic commands ###
