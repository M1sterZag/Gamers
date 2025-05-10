"""reset migrations

Revision ID: 5e94d1e732a1
Revises: 9873e5ab5d76
Create Date: 2025-05-10 20:37:44.248259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e94d1e732a1'
down_revision: Union[str, None] = '9873e5ab5d76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
