"""step2_add_default_email

Revision ID: 1411cd4d155a
Revises: d014556d0781
Create Date: 2024-10-16 22:53:37.097983

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1411cd4d155a"
down_revision: Union[str, None] = "d014556d0781"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE customers SET email = 'default@example.com' WHERE email IS NULL")


def downgrade() -> None:
    op.execute("UPDATE customers SET email = NULL WHERE email = 'default@example.com'")
