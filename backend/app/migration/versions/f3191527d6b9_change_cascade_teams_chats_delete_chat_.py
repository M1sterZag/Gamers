"""change cascade teams chats + delete chat_id(teams) + add team_id(chats)

Revision ID: f3191527d6b9
Revises: f54c3cca4bbc
Create Date: 2025-02-27 18:53:11.071906

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3191527d6b9'
down_revision: Union[str, None] = 'f54c3cca4bbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chats', sa.Column('team_id', sa.Integer(), nullable=True))
    op.drop_constraint('chats_owner_id_fkey', 'chats', type_='foreignkey')
    op.create_foreign_key(None, 'chats', 'teams', ['team_id'], ['id'])
    op.drop_column('chats', 'owner_id')
    op.drop_constraint('teams_chat_id_fkey', 'teams', type_='foreignkey')
    op.drop_column('teams', 'chat_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('chat_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('teams_chat_id_fkey', 'teams', 'chats', ['chat_id'], ['id'])
    op.add_column('chats', sa.Column('owner_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'chats', type_='foreignkey')
    op.create_foreign_key('chats_owner_id_fkey', 'chats', 'users', ['owner_id'], ['id'])
    op.drop_column('chats', 'team_id')
    # ### end Alembic commands ###
