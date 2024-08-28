from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.orm.base import Base


class UserORM(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    blogs = relationship("BlogORM", back_populates="user")
