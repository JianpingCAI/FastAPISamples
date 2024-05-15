# This Jinja2 template generates SQLAlchemy and Pydantic model classes #
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

Base = declarative_base()


# Association Tables
testsuite_testcase_m2m = Table(
    'testsuite_testcase_m2m', 
    Base.metadata,
    Column('test_suite_id', Integer, ForeignKey('testsuite.id'), primary_key=True),
    Column('test_case_id', Integer, ForeignKey('testcase.id'), primary_key=True),
    )


# SQLAlchemy Model
class TestSuite(Base):
    __tablename__ = "testsuite"

    # Sequence required by DuckDB, due to its lack of support for `SERIAL` used by SQLAlchemy for auto-increment
    testsuite_id_seq = Sequence("testsuite_id_seq")
    id = Column(
        Integer,
        "testsuite_id_seq",
        server_default=testsuite_id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String(255), primary_key=False, index=False, nullable=False)
    description = Column(Text, primary_key=False, index=False, nullable=True)

    # Relationships

    testcases = relationship("TestCase",secondary="testsuite_testcase_m2m",back_populates="test_suites")
# Pydantic Models
class TestSuiteBase(BaseModel):
    name: Optional[str] = None
    description: Optional[Optional[str]] = None


class TestSuiteCreate(TestSuiteBase):
    pass


class TestSuiteDB(TestSuiteBase):
    id: int

    # Relationships
    from .testcase import TestCaseDB
    testcases: List[TestCaseDB]
    
    class Config:
        from_attributes = True