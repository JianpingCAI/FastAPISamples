# This Jinja2 template generates SQLAlchemy and Pydantic model classes #
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Sequence, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

Base = declarative_base()



# SQLAlchemy Model
class TestCase(Base):
    __tablename__ = "testcase"

    # Sequence required by DuckDB, due to its lack of support for `SERIAL` used by SQLAlchemy for auto-increment
    testcase_id_seq = Sequence("testcase_id_seq")
    id = Column(
        Integer,
        "testcase_id_seq",
        server_default=testcase_id_seq.next_value(),
        primary_key=True,
    )
    description = Column(Text, primary_key=False, index=False, nullable=True)

    # Relationships

    testsuites = relationship("TestSuite",secondary="testsuite_testcase_m2m",back_populates="test_cases")
# Pydantic Models
class TestCaseBase(BaseModel):
    description: Optional[Optional[str]] = None


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseDB(TestCaseBase):
    id: int

    # Relationships
    from .testsuite import TestSuiteDB
    testsuites: List[TestSuiteDB]
    
    class Config:
        from_attributes = True