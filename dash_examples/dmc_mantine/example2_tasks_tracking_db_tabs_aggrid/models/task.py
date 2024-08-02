from sqlalchemy import Column, Integer, String
from pydantic import BaseModel

from .database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_name = Column(String, index=True)
    description = Column(String)
    due_date = Column(String)
    status = Column(String, default="Pending")


class TaskCreate(BaseModel):
    task_name: str
    description: str
    due_date: str


class TaskUpdate(BaseModel):
    id: int
    status: str
