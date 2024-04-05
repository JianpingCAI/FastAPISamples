# This Jinja2 template generates SQLAlchemy and Pydantic model classes #
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

Base = declarative_base()


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
    project_id = Column(Integer, primary_key=False, index=False, nullable=True)
    created_at = Column(DateTime, primary_key=False, index=False, nullable=False)
    updated_at = Column(DateTime, primary_key=False, index=False, nullable=False)


# Pydantic Models
class TestSuiteBase(BaseModel):
    name: Optional[str] = None
    description: Optional[Optional[str]] = None
    project_id: Optional[Optional[int]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class TestSuiteCreate(TestSuiteBase):
    pass


class TestSuiteDB(TestSuiteBase):
    id: int

    class Config:
        from_attributes = True