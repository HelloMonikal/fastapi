"""add users table

Revision ID: b7862141f272
Revises: 5f443e9ffab4
Create Date: 2024-08-18 15:34:11.362493

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7862141f272'
down_revision: Union[str, None] = '5f443e9ffab4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users"
                    ,sa.Column("id",sa.Integer(),nullable=False)
                    ,sa.Column("email",sa.String(),nullable=False)
                    ,sa.Column("password",sa.String(),nullable=False)
                    ,sa.Column("created_at",sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"),nullable=False)
                    ,sa.PrimaryKeyConstraint("id")
                    ,sa.UniqueConstraint("email")
                    )
    pass



def downgrade() -> None:
    op.drop_table("users")
    pass
