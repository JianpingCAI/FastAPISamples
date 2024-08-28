from typing import List
from sqlalchemy.orm import Session
from infrastructure.orm.comment_mapper import CommentORM
from domain.models.comment import Comment


class CommentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, comment: Comment) -> None:
        comment_orm = CommentORM(
            content=comment.content, post_id=comment.post.id, user_id=comment.user.id
        )
        self.db_session.add(comment_orm)
        self.db_session.commit()

    def find_by_post_id(self, post_id: int) -> List[Comment]:
        comments_orm = (
            self.db_session.query(CommentORM)
            .filter(CommentORM.post_id == post_id)
            .all()
        )
        return [
            Comment(
                id=comment.id,
                content=comment.content,
                user=comment.user,
                post=comment.post,
            )
            for comment in comments_orm
        ]
