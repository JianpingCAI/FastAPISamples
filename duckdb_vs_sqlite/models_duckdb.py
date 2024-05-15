# https://github.com/Mause/duckdb_engine/issues/939
# https://github.com/Mause/duckdb_engine
# https://dev.to/astrojuanlu/the-simplicity-of-duckdb-3lad
# https://docs.sqlalchemy.org/en/20/dialects/
# dialect duckdb+duckdb_engine does not support caching

## version info: duckdb_engine 0.11.3
## Issue: there should not be `index=True` in the class field
## Related issue: //github.com/Mause/duckdb_engine/issues/939


from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Sequence,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

# Database connection setup (Update as per your database)
# engine = create_engine("duckdb:///:memory:", echo=True)
engine = create_engine("duckdb:///./relationships.db", echo=True)

Base = declarative_base()

# Junction table for TestSuite and TestCase many-to-many relationship
suite_case_association = Table(
    "suite_case",
    Base.metadata,
    Column("test_suite_id", Integer, ForeignKey("test_suites.id")),
    Column("test_case_id", Integer, ForeignKey("test_cases.id")),
)


# TestSuite model
id_seq1 = Sequence("id_seq1")
class TestSuite(Base):
    __tablename__ = "test_suites"
    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        id_seq1,
        server_default=id_seq1.next_value(),
        primary_key=True,
    )
    name = Column(String)
    description = Column(String)
    test_cases = relationship(
        "TestCase", secondary=suite_case_association, back_populates="test_suites"
    )


# TestCase model
id_seq2 = Sequence("id_seq")
class TestCase(Base):
    __tablename__ = "test_cases"
    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        id_seq2,
        server_default=id_seq1.next_value(),
        primary_key=True,
    )
    name = Column(String)
    description = Column(String)
    expected_outcome = Column(String)
    test_suites = relationship(
        "TestSuite", secondary=suite_case_association, back_populates="test_cases"
    )


Base.metadata.create_all(engine)
