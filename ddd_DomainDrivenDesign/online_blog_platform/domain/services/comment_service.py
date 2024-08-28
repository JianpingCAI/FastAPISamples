from typing import List, Optional
from domain.models.user import User
from domain.models.comment import Comment
from domain.models.post import Post
from domain.repositories.comment_repository import CommentRepository


class CommentService:
    def __init__(self, comment_repository: CommentRepository):
        self.comment_repository = comment_repository

    def add_comment(self, content: str, user: User, post: Post) -> Comment:
        comment = Comment(content=content, user=user, post=post)
        post.add_comment(comment)
        self.comment_repository.save(comment)
        return comment

    def get_comments_for_post(self, post_id: int) -> List[Comment]:
        return self.comment_repository.find_by_post_id(post_id)
