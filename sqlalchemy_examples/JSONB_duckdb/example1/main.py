import sqlalchemy as sa
import duckdb

# Establish a connection to DuckDB using SQLAlchemy
engine = sa.create_engine("duckdb:///")

# Define metadata object
metadata = sa.MetaData()

# Define a table with JSONB column
test_table = sa.Table(
    "test_table",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("data", sa.JSON),  # SQLAlchemy uses JSON which maps to JSONB in DuckDB
)

# Create the table in the database
metadata.create_all(engine)

# Insert JSON data into the table
with engine.connect() as conn:
    conn.execute(
        test_table.insert(),
        [
            {"id": 1, "data": {"name": "Alice", "age": 30}},
            {"id": 2, "data": {"name": "Bob", "age": 25}},
        ],
    )

    # Query the data
    result = conn.execute(sa.select(test_table.c.data["name"])).fetchall()
    print("Names in JSON data:", result)

    # Query using JSON functions
    result = conn.execute(
        sa.select(test_table.c.data).where(
            test_table.c.data["age"].astext.cast(sa.Integer) > 27
        )
    ).fetchall()
    print("Entries where age > 27:", result)
