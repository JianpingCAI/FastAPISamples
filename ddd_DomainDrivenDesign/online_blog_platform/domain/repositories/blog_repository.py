from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.orm.blog_mapper import BlogORM
from domain.models.blog import Blog
from domain.models.user import User


class BlogRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, blog: Blog) -> None:
        blog_orm = BlogORM(
            title=blog.title, description=blog.description, user_id=blog.user.id
        )
        self.db_session.add(blog_orm)
        self.db_session.commit()

    def find_by_id(self, blog_id: int) -> Optional[Blog]:
        blog_orm = self.db_session.query(BlogORM).filter(BlogORM.id == blog_id).first()
        if blog_orm:
            user = User(
                id=blog_orm.user.id,
                username=blog_orm.user.username,
                email=blog_orm.user.email,
                password=blog_orm.user.password,
            )
            return Blog(
                id=blog_orm.id,
                title=blog_orm.title,
                description=blog_orm.description,
                user=user,
            )
        return None
