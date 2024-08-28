from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.orm.base import Base


class PostORM(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    blog_id = Column(Integer, ForeignKey("blogorm.id"))
    
    blog = relationship("BlogORM", back_populates="posts")
    comments = relationship("CommentORM", back_populates="post")
