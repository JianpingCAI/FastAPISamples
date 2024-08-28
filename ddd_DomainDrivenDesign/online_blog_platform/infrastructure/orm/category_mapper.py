from sqlalchemy import Column, Integer, String
from infrastructure.orm.base import Base


class CategoryORM(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
