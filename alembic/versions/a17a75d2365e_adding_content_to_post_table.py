"""adding content to post table

Revision ID: a17a75d2365e
Revises: abbdb7259b36
Create Date: 2024-07-31 11:01:09.798845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a17a75d2365e'
down_revision: Union[str, None] = 'abbdb7259b36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
