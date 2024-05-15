###############################################
# CRUD operations

from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, exc
from typing import List, Dict, Any
import sqlalchemy as sa

# Define the base class
Base = declarative_base()


id_seq1 = sa.Sequence("id_seq1")


# Define the table structure
class RecordDB(Base):
    __tablename__ = "record_table"
    id: int = Column(
        Integer, id_seq1, primary_key=True, server_default=id_seq1.next_value()
    )
    data: Dict[str, Any] = Column(
        sa.JSON
    )  # JSON type in SQLAlchemy corresponds to JSONB in DuckDB


# Create an engine and bind it to the session
engine = sa.create_engine("duckdb:///:memory:")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# CREATE: Insert JSON data into the table
session.add_all(
    [
        RecordDB(id=1, data={"name": "Alice", "age": 30}),
        RecordDB(id=2, data={"name": "Bob", "age": 25}),
    ]
)
session.commit()

# READ: Query the data
names: List[str] = session.query(RecordDB.data["name"]).all()
print("Names in JSON data:", names)

# UPDATE: Update a record
try:
    record_to_update: RecordDB = session.query(RecordDB).filter(RecordDB.id == 1).one()
    record_to_update.data["age"] = 31
    session.commit()
    print(f"Updated age for Alice: {record_to_update.data['age']}")
except exc.NoResultFound:
    print("Record not found.")

# DELETE: Delete a record
try:
    record_to_delete: RecordDB = session.query(RecordDB).filter(RecordDB.id == 2).one()
    session.delete(record_to_delete)
    session.commit()
    print("Record deleted successfully.")
except exc.NoResultFound:
    print("Record to delete not found.")

# Verify changes
results: List[RecordDB] = session.query(RecordDB).all()
print("Remaining records after update and delete operations:")
for result in results:
    print(f"ID: {result.id}, Data: {result.data}")

# Close the session
session.close()
