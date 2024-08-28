from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.orm.base import Base


class BlogORM(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("userorm.id"))

    user = relationship("UserORM", back_populates="blogs")
    posts = relationship("PostORM", back_populates="blog")
