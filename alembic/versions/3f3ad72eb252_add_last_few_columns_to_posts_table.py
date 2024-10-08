"""add last few columns to posts table

Revision ID: 3f3ad72eb252
Revises: df9e3e4c77f2
Create Date: 2024-08-18 15:51:32.388658

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f3ad72eb252'
down_revision: Union[str, None] = 'df9e3e4c77f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published",sa.Boolean(),nullable=False,server_default="TRUE"))
    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
