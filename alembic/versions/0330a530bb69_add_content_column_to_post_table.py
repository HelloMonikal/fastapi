"""add content column to post table

Revision ID: 0330a530bb69
Revises: df59833401db
Create Date: 2025-10-07 15:28:42.236342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0330a530bb69'
down_revision: Union[str, None] = 'df59833401db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False, server_default=""))
    pass

def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
