"""change payment id to uuid

Revision ID: 9873e5ab5d76
Revises: 54a9a6d58642
Create Date: 2025-05-06 12:49:04.058400

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9873e5ab5d76'
down_revision: Union[str, None] = '54a9a6d58642'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('user_subscriptions', 'payment_id')
    op.add_column('user_subscriptions',
                  sa.Column('payment_id', postgresql.UUID(as_uuid=True), nullable=False))


def downgrade():
    op.drop_column('user_subscriptions', 'payment_id')
    op.add_column('user_subscriptions',
                  sa.Column('payment_id', sa.INTEGER(), nullable=False))
