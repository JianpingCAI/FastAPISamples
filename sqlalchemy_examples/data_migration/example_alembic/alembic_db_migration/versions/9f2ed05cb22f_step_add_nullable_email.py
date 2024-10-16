"""step_add nullable email

Revision ID: 9f2ed05cb22f
Revises: d0034c73b214
Create Date: 2024-10-16 22:44:22.578040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9f2ed05cb22f'
down_revision: Union[str, None] = 'd0034c73b214'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
