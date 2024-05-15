###############################################
# simple example of JSONB in DuckDB

from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa
import duckdb

# Define the base class
Base = declarative_base()

id_seq1 = sa.Sequence("id_seq1")


# Define the table structure
class Record(Base):
    __tablename__ = "test_table"
    # id = Column(Integer, primary_key=True)
    id = Column(Integer, id_seq1, server_default=id_seq1.next_value(), primary_key=True)
    data = Column(sa.JSON)  # JSON type in SQLAlchemy corresponds to JSONB in DuckDB


# Create an engine and bind it to the session
engine = create_engine("duckdb:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Insert JSON data into the table
session.add_all(
    [
        Record(id=1, data={"name": "Alice", "age": 30}),
        Record(id=2, data={"name": "Bob", "age": 25}),
    ]
)
session.commit()

# Query the data
results = session.query(Record.data["name"]).all()
# print("Names in JSON data:", results)
print("Names in JSON data:", [result[0] for result in results])


# Query using JSON functions, filtering by age
results = (
    session.query(Record.data)
    .filter(sa.cast(Record.data["age"], Integer) > 27)
    .all()
)
print("Entries where age > 27:", [result[0] for result in results])

# Close the session
session.close()
