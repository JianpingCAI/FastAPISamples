"""step3_create_temp_customers

Revision ID: 245927cd0211
Revises: 1411cd4d155a
Create Date: 2024-10-16 22:58:30.819018

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "245927cd0211"
down_revision: Union[str, None] = "1411cd4d155a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Using Alembic operations to create the new_orders table
    # op.create_table('customers',
    # sa.Column('id', sa.Integer(), nullable=False),
    # sa.Column('name', sa.String(), nullable=False),
    # sa.PrimaryKeyConstraint('id')
    # )
    # Use raw SQL to create the table to ensure compatibility with DuckDB
    op.execute(
        """
        CREATE TABLE temp_customers (
            id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
        )
    """
    )
    # Note: No 'AUTOINCREMENT' keyword is necessary because DuckDB treats INTEGER PRIMARY KEY as auto-incrementing

    # 2. Copy data from the old table to the new table
    op.execute(
        "INSERT INTO temp_customers (id, name, email) SELECT id, name, email FROM customers"
    )


def downgrade() -> None:
    op.drop_table("temp_customers")
