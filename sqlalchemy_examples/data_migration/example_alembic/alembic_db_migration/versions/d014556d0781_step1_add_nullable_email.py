"""step1_add nullable email

Revision ID: d014556d0781
Revises: 9f2ed05cb22f
Create Date: 2024-10-16 22:48:37.779919

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd014556d0781'
down_revision: Union[str, None] = '9f2ed05cb22f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add column as nullable
    op.add_column("customers", sa.Column("email", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "email")
