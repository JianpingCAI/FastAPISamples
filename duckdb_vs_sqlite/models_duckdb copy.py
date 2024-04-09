from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Sequence,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Database connection setup (Update as per your database)
# engine = create_engine('sqlite:///test_system.db', echo=True)
engine = create_engine("duckdb:///test_system_duck.db", echo=True)

Base = declarative_base()

# Junction table for TestSuite and TestCase many-to-many relationship
suite_case_association = Table(
    'suite_case_association', Base.metadata,
    Column('test_suite_id', Integer, ForeignKey('test_suites.id'), primary_key=True),
    Column('test_case_id', Integer, ForeignKey('test_cases.id'), primary_key=True)
)

# # Junction table for TestSuite and Tag
# test_suite_tags = Table(
#     'test_suite_tags', Base.metadata,
#     Column('test_suite_id', Integer, ForeignKey('test_suites.id'), primary_key=True),
#     Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
# )


# # Junction table for TestCase and Tag
# test_case_tags = Table(
#     'test_case_tags', Base.metadata,
#     Column('test_case_id', Integer, ForeignKey('test_cases.id'), primary_key=True),
#     Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
# )

# TestSuite model
class TestSuite(Base):
    __tablename__ = "test_suites"
    # id = Column(Integer, primary_key=True)
    id_seq = Sequence("id_seq")
    id = Column(
        Integer,
        id_seq,
        server_default=id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String, index=True)
    description = Column(String)
    test_cases = relationship(
        "TestCase", secondary=suite_case_association, back_populates="test_suites"
    )
    # tags = relationship("Tag", secondary=test_suite_tags, back_populates="test_suites")


# TestCase model
class TestCase(Base):
    __tablename__ = "test_cases"
    # id = Column(Integer, primary_key=True)
    id_seq = Sequence("id_seq")
    id = Column(
        Integer,
        id_seq,
        server_default=id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String, index=True)
    description = Column(String)
    expected_outcome = Column(String)
    test_suites = relationship(
        "TestSuite", secondary=suite_case_association, back_populates="test_cases"
    )
    # tags = relationship("Tag", secondary=test_case_tags, back_populates="test_cases")


# # Tag model
# class Tag(Base):
#     __tablename__ = "tags"
#     # id = Column(Integer, primary_key=True)
#     id_seq = Sequence("id_seq")
#     id = Column(
#         Integer,
#         id_seq,
#         server_default=id_seq.next_value(),
#         primary_key=True,
#     )
#     name = Column(String, index=True)
#     tag_type = Column(String, index=True)
#     test_suites = relationship(
#         "TestSuite", secondary=test_suite_tags, back_populates="tags"
#     )
#     test_cases = relationship(
#         "TestCase", secondary=test_case_tags, back_populates="tags"
#     )


# Create all tables in the engine
Base.metadata.create_all(engine)


# class suite_case_association(Base):
#     __tablename__ = "suite_case_association"
#     test_suite_id = Column(
#         "test_suite_id", Integer, ForeignKey("test_suites.id"), primary_key=True
#     )
#     test_case_id = Column(
#         "test_case_id", Integer, ForeignKey("test_cases.id"), primary_key=True
#     )


# class test_suite_tags(Base):
#     __tablename__ = "test_suite_tags"
#     test_suite_id = Column(
#         "test_suite_id", Integer, ForeignKey("test_suites.id"), primary_key=True
#     )
#     test_case_id = Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)


# class test_case_tags(Base):
#     __tablename__ = "test_case_tags"
#     test_suite_id = Column(
#         "test_case_id", Integer, ForeignKey("test_cases.id"), primary_key=True
#     )
#     test_case_id = Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
