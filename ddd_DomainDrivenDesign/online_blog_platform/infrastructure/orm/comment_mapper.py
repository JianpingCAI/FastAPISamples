from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.orm.base import Base


class CommentORM(Base):
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    post_id = Column(Integer, ForeignKey("postorm.id"))
    user_id = Column(Integer, ForeignKey("userorm.id"))

    post = relationship("PostORM", back_populates="comments")
    user = relationship("UserORM")
