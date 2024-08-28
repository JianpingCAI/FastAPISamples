from typing import Optional, List
from sqlalchemy.orm import Session
from domain.models.comment import Comment
from domain.services.comment_service import CommentService

class CommentManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.comment_service = CommentService(db_session)

    def add_comment(self, post_id: int, user_id: int, content: str) -> Comment:
        # Business logic to add a comment to a post
        comment = self.comment_service.add_comment(content, user_id, post_id)
        return comment

    def get_comments_for_post(self, post_id: int) -> List[Comment]:
        # Business logic to retrieve all comments for a post
        comments = self.comment_service.get_comments_for_post(post_id)
        return comments
