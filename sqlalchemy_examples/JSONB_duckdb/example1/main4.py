from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy.orm import declarative_base
import sqlalchemy as sa
import duckdb
from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List, Optional


# Define the Pydantic model for the JSON data
class Record(BaseModel):
    name: str
    age: int


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


# Set up the database connection and session
engine = create_engine("duckdb:///:memory:")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


# CRUD operation functions
def create_user(session: sessionmaker, user_data: Record, user_id: int) -> None:
    """Create a new user record."""
    session.add(RecordDB(id=user_id, data=user_data.model_dump()))
    session.commit()


def read_user(session: sessionmaker, user_id: int) -> Optional[Record]:
    """Read user data by ID."""
    try:
        result = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        return Record(**result.data)
    except exc.NoResultFound:
        return None


def update_user(session: sessionmaker, user_id: int, new_data: Record) -> None:
    """Update existing user data."""
    try:
        record = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        record.data = new_data.model_dump()
        session.commit()
    except exc.NoResultFound:
        print("Record not found.")


def delete_user(session: sessionmaker, user_id: int) -> None:
    """Delete a user record."""
    try:
        record_to_delete = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        session.delete(record_to_delete)
        session.commit()
    except exc.NoResultFound:
        print("Record to delete not found.")


def main():
    session = Session()

    # Example data
    alice = Record(name="Alice", age=30)
    bob = Record(name="Bob", age=25)

    # Create records
    create_user(session, alice, 1)
    create_user(session, bob, 2)

    # Read and print user
    user = read_user(session, 1)
    if user:
        print("Read User:", user.model_dump())

    # Update user
    alice_updated = Record(name="Alice", age=31)
    update_user(session, 1, alice_updated)
    # Read and print user
    user = read_user(session, 1)
    if user:
        print("Read User:", user.model_dump())

    # Delete user
    delete_user(session, 2)

    # Cleanup
    session.close()


if __name__ == "__main__":
    main()
