from sqlalchemy import create_engine, Column, Integer, JSON, String, cast, Sequence
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.sql import text
from sqlalchemy import exc


# Define the Pydantic model for the JSON data
class Record(BaseModel):
    name: str
    age: int


# Define the base class
Base = declarative_base()

id_seq1 = Sequence("id_seq1")


# Define the table structure
class RecordDB(Base):
    __tablename__ = "record_table"
    id: int = Column(
        Integer, id_seq1, primary_key=True, server_default=id_seq1.next_value()
    )
    data = Column(JSON, nullable=False)


# Set up the database connection and session
engine = create_engine("duckdb:///:memory:", echo=False)
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


# CRUD operation functions
def create_user(session, user_data: Record, user_id: Optional[int] = None) -> None:
    """Create a new user record."""
    try:
        session.add(RecordDB(id=user_id, data=user_data.model_dump()))
        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error creating user: {e}")


def read_user(session, user_id: int) -> Optional[Record]:
    """Read user data by ID."""
    try:
        result = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        return Record(**result.data)
    except exc.NoResultFound:
        return None


def update_user(session, user_id: int, new_data: Record) -> None:
    """Update existing user data."""
    try:
        record = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        record.data = new_data.model_dump()
        session.commit()
    except exc.NoResultFound:
        print("Record not found.")


def delete_user(session, user_id: int) -> None:
    """Delete a user record."""
    try:
        record_to_delete = session.query(RecordDB).filter(RecordDB.id == user_id).one()
        session.delete(record_to_delete)
        session.commit()

        print("delete User:", record_to_delete.data)
    except exc.NoResultFound:
        print("Record to delete not found.")


def find_user_by_name(session, name: str) -> List[Record]:
    """Find user(s) by name."""
    try:
        results = (
            session.query(RecordDB)
            .filter(cast(RecordDB.data["name"], String) == name)
            .all()
        )
        return [Record(**result.data) for result in results]
    except SQLAlchemyError as e:
        print(f"Error finding user by name: {e}")
        return []


import json


#####################
## Method: not working for sqlite and duckdb
def find_user_by_name1(session, name: str) -> List[Record]:
    """Find user(s) by name."""
    try:
        results = (
            session.query(RecordDB)
            .filter(cast(RecordDB.data["name"], String) == name)
            .all()
        )
        return [Record(**result.data) for result in results]
    except SQLAlchemyError as e:
        print(f"Error finding user by name: {e}")
        return []


#####################
## Method: working for sqlite
# def find_user_by_name(session, name: str) -> List[Record]:
#     """Find user(s) by name."""
#     try:
#         # Directly access JSON field using JSON_EXTRACT
#         query = text(
#             "SELECT * FROM record_table WHERE json_extract(data, '$.name') = :name"
#         )
#         results = session.execute(query, {"name": name}).fetchall()
#         return [Record(**json.loads(row._mapping["data"])) for row in results]
#     except SQLAlchemyError as e:
#         print(f"Error finding user by name: {e}")
#         return []


#####################
## Method: working for duckdb
def find_user_by_name2(session, name: str) -> List[Record]:
    """Find user(s) by name."""
    try:
        # Directly access JSON field using json_extract_string
        query = text(
            "SELECT * FROM record_table WHERE json_extract_string(data, '$.name') = :name"
        )
        results = session.execute(query, {"name": name}).fetchall()
        return [Record(**row._mapping["data"]) for row in results]
    except SQLAlchemyError as e:
        print(f"Error finding user by name: {e}")
        return []


def find_user_by_age(session, age: int) -> List[Record]:
    """Find user(s) by age."""
    try:
        results = (
            session.query(RecordDB)
            .filter(cast(RecordDB.data["age"], Integer) == age)
            .all()
        )
        return [Record(**result.data) for result in results]
    except SQLAlchemyError as e:
        print(f"Error finding user by age: {e}")
        return []


def verify_data_storage(session):
    records = session.query(RecordDB).all()
    for record in records:
        print(record.data)


def main():
    session = Session()

    # Example data
    alice = Record(name="Alice", age=30)
    bob = Record(name="Bob", age=25)
    jp = Record(name="JP", age=38)

    # Create records
    create_user(session, alice)
    create_user(session, bob)
    create_user(session, jp)

    verify_data_storage(session)

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
        print("Updated User:", user.model_dump())

    # Delete user
    delete_user(session, 2)

    results: List[RecordDB] = session.query(RecordDB).all()
    print("Remaining records after update and delete operations:")
    for result in results:
        print(f"ID: {result.id}, Data: {result.data}")

    # Find user by name
    users_by_name: List[Record] = find_user_by_name1(session, "JP")
    print(
        "??? method1 (fails)-Found Users by name:",
        [user.model_dump() for user in users_by_name],
    )

    # Find user by name
    users_by_name: List[Record] = find_user_by_name2(session, "JP")
    print("method2-Found Users by name:", [user.model_dump() for user in users_by_name])

    # Find user by age
    users_by_age: List[Record] = find_user_by_age(session, 38)
    print("Found Users by age:", [user.model_dump() for user in users_by_age])

    # Cleanup
    session.close()


if __name__ == "__main__":
    main()
