"""add content column to post table

Revision ID: 5f443e9ffab4
Revises: 01365a2f054f
Create Date: 2024-08-18 15:27:42.922008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f443e9ffab4'
down_revision: Union[str, None] = '01365a2f054f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",
                  sa.Column("content",sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
