# Steps

## Initialize alembic

```shell
alembic init alembic_db_migration
```

## orm/models.py

```python
from sqlalchemy import (
    Sequence,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Declare the base
Base = declarative_base()

custom_id_seq = Sequence("custom_id_seq")
order_id_seq = Sequence("order_id_seq")


class Customer(Base):
    __tablename__ = "customers"

    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        custom_id_seq,
        server_default=custom_id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        order_id_seq,
        server_default=order_id_seq.next_value(),
        primary_key=True,
    )
    item_name = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")


Customer.orders = relationship("Order", order_by=Order.id, back_populates="customer")

# Set up the database engine
engine = create_engine("duckdb:///test_duckdb.db", echo=False)

# Create all tables in the database
Base.metadata.create_all(engine)
```

## orm/__init__.py

## Edit alembic.ini

```ini
sqlalchemy.url = duckdb:///test_duckdb.db
```

## Edit alembic_db_migration/env.py

``` python
from orm.models import Base
target_metadata = Base.metadata

```

For DuckDB, the following lines should also be added;otherwise, there will be error message: KeyError: 'duckdb'

```python
# Jianping
from alembic.ddl.impl import DefaultImpl


# Jianping: https://github.com/Mause/duckdb_engine
class AlembicDuckDBImpl(DefaultImpl):
    """Alembic implementation for DuckDB."""

    __dialect__ = "duckdb"
```

## Generate ugprade script using alembic

``` shell
alembic revision -m "Initial database setup" --autogenerate
```

A file `./alembic_db_migration/versions/d0034c73b214_initial_database_setup.py` will be generated.

## Run migrations

``` shell
alembic upgrade head
```

The database file is created.

## Test the created database in `main.py`

```python
from orm.models import sessionmaker, engine, Customer, Order

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Example usage
new_customer = Customer(name="John Doe")
session.add(new_customer)
session.commit()

# Querying data
customers = session.query(Customer).all()
for customer in customers:
    print(customer.id, customer.name)
```

## Add an email column to the `Customer` table

### orm/models.py

```python
    email = Column(String, nullable=False)
```

### Generate ugprade script using alembic

``` shell
alembic revision -m "add email to customers" --autogenerate
```

### Migrate the database

```shell
alembic upgrade head
```

#### Error occurs to DuckDB

"""
sqlalchemy.exc.ProgrammingError: (duckdb.duckdb.ParserException) Parser Error: Adding columns with constraints not yet supported
[SQL: ALTER TABLE customers ADD COLUMN email VARCHAR NOT NULL]
(Background on this error at: <https://sqlalche.me/e/20/f405>)
"""

#### Solution

```shell
alembic revision -m "step_add nullable email"
```

```python
def upgrade() -> None:
    # Step 1: Add column as nullable
    op.add_column("customers", sa.Column("email", sa.String(255), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "email")

```

```shell
alembic upgrade head
```

```shell
alembic revision -m "step2_add_default_email"
```

```python

def upgrade() -> None:
    op.execute("UPDATE customers SET email = 'default@example.com' WHERE email IS NULL")


def downgrade() -> None:
    op.execute("UPDATE customers SET email = NULL WHERE email = 'default@example.com'")
```

```shell
alembic upgrade head
```

Create a `temp_customers` table with not-nullable email column, and copy data from "customers" to "temp_customers".

```python
# Using Alembic operations to create the new_orders table
    # op.create_table(
    #     'new_orders',
    #     sa.Column('id', sa.Integer(), nullable=False, primary_key=True),  # Correct auto-increment definition
    #     sa.Column('item_name', sa.String(), nullable=False),
    #     sa.Column('customer_id', sa.Integer(), nullable=False),
    #     sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
    #     sqlite_autoincrement=True  # Ensures autoincrement is properly handled in SQLite and compatible DBs like DuckDB
    # )
     # Use raw SQL to create the table to ensure compatibility with DuckDB
    op.execute("""
        CREATE TABLE new_orders (
            id INTEGER PRIMARY KEY,
            item_name VARCHAR NOT NULL,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY(customer_id) REFERENCES customers(id)
        )
    """)
    # Note: No 'AUTOINCREMENT' keyword is necessary because DuckDB treats INTEGER PRIMARY KEY as auto-incrementing

```

```shell
alembic upgrade head
```

Due to DuckDB limitations (cannot drop foreign key constraint), we need to drop `orders` table first.

``` python
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

```
