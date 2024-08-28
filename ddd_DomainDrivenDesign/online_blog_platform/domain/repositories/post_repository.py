from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.orm.post_mapper import PostORM
from domain.models.post import Post
from domain.models.blog import Blog


class PostRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, post: Post) -> None:
        post_orm = PostORM(title=post.title, content=post.content, blog_id=post.blog.id)
        self.db_session.add(post_orm)
        self.db_session.commit()

    def find_by_id(self, post_id: int) -> Optional[Post]:
        post_orm = self.db_session.query(PostORM).filter(PostORM.id == post_id).first()
        if post_orm:
            blog = Blog(
                id=post_orm.blog.id,
                title=post_orm.blog.title,
                description=post_orm.blog.description,
                user_id=post_orm.blog.user_id,
            )

            return Post(
                id=post_orm.id,
                title=post_orm.title,
                content=post_orm.content,
                blog_id=blog.id,
            )
        return None
