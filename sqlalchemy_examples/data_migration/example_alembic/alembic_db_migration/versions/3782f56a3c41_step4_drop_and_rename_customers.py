"""step4 drop and rename customers

Revision ID: 3782f56a3c41
Revises: 245927cd0211
Create Date: 2024-10-16 23:10:06.004198

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine.reflection import Inspector  # Ensure this import is included


# revision identifiers, used by Alembic.
revision: str = "3782f56a3c41"
down_revision: Union[str, None] = "245927cd0211"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Backup the old table by renaming it
    # op.rename_table("orders", "orders_backup")
    # op.drop_constraint('customer.id', 'orders', type_='foreignkey')
    # op.execute("ALTER TABLE orders DROP CONSTRAINT 'customer.id'")
    op.drop_table("orders")

    op.rename_table("customers", "customers_backup")

    # # Drop the old 'customers' table if needed or do other operations
    # op.drop_table("customers_backup")

    # Rename the new table to the old table's name
    op.rename_table("temp_customers", "customers")

    # op.rename_table("orders_backup", "orders")


def downgrade() -> None:
    pass
