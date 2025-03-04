"""add new tables + add check constraint on team(time)

Revision ID: 428b0e4eb7ba
Revises: 74fa6cc12596
Create Date: 2025-02-24 17:19:43.228857

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '428b0e4eb7ba'
down_revision: Union[str, None] = '74fa6cc12596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.VARCHAR(length=255),
               type_=sa.String(length=60),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'username',
               existing_type=sa.String(length=60),
               type_=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
