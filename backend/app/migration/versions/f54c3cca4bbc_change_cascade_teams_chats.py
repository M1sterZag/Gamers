"""change cascade teams chats

Revision ID: f54c3cca4bbc
Revises: f95abc6a3d37
Create Date: 2025-02-27 18:25:41.050579

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f54c3cca4bbc'
down_revision: Union[str, None] = 'f95abc6a3d37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('chat_members_chat_id_fkey', 'chat_members', type_='foreignkey')
    op.create_foreign_key(None, 'chat_members', 'chats', ['chat_id'], ['id'])
    op.drop_constraint('messages_chat_id_fkey', 'messages', type_='foreignkey')
    op.create_foreign_key(None, 'messages', 'chats', ['chat_id'], ['id'])
    op.drop_constraint('team_members_team_id_fkey', 'team_members', type_='foreignkey')
    op.create_foreign_key(None, 'team_members', 'teams', ['team_id'], ['id'])
    op.drop_constraint('teams_chat_id_fkey', 'teams', type_='foreignkey')
    op.create_foreign_key(None, 'teams', 'chats', ['chat_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'teams', type_='foreignkey')
    op.create_foreign_key('teams_chat_id_fkey', 'teams', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'team_members', type_='foreignkey')
    op.create_foreign_key('team_members_team_id_fkey', 'team_members', 'teams', ['team_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'messages', type_='foreignkey')
    op.create_foreign_key('messages_chat_id_fkey', 'messages', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint(None, 'chat_members', type_='foreignkey')
    op.create_foreign_key('chat_members_chat_id_fkey', 'chat_members', 'chats', ['chat_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
