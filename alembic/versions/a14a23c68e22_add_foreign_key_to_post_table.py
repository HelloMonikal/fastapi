"""add foreign key to post table

Revision ID: a14a23c68e22
Revises: ebf5f5b3e2f9
Create Date: 2025-10-07 15:38:04.750033

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a14a23c68e22'
down_revision: Union[str, None] = 'ebf5f5b3e2f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts'
                          , referent_table='users', local_cols=['owner_id']
                          , remote_cols=['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
