"""add foreign key to post table

Revision ID: df9e3e4c77f2
Revises: b7862141f272
Create Date: 2024-08-18 15:44:57.831611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df9e3e4c77f2'
down_revision: Union[str, None] = 'b7862141f272'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key("post_user_fk",source_table="posts",referent_table="users"
                          ,local_cols=["owner_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_user_fk",table_name="posts")
    op.drop_column("posts","owner_id")
    pass
