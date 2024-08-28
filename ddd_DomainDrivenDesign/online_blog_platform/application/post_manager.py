from typing import Optional
from sqlalchemy.orm import Session
from domain.models.post import Post
from domain.models.comment import Comment
from domain.services.post_service import PostService
from domain.services.comment_service import CommentService

class PostManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.post_service = PostService(db_session)
        self.comment_service = CommentService(db_session)

    def create_post(self, blog_id: int, title: str, content: str) -> Post:
        # Business logic to create a post
        post = self.post_service.create_post(title, content, blog_id)
        return post

    def get_post(self, post_id: int) -> Optional[Post]:
        # Business logic to retrieve a post
        post = self.post_service.get_post_by_id(post_id)
        return post

    def update_post(self, post_id: int, title: str, content: str) -> Optional[Post]:
        # Ensure the post exists before updating
        post = self.get_post(post_id)
        if not post:
            raise ValueError("Post not found")

        # Business logic to update a post
        updated_post = self.post_service.update_post(post, title, content)
        return updated_post

    def delete_post(self, post_id: int) -> None:
        # Ensure the post exists before deleting
        post = self.get_post(post_id)
        if not post:
            raise ValueError("Post not found")

        # Business logic to delete a post
        self.post_service.delete_post(post)

    def add_comment_to_post(self, post_id: int, user_id: int, content: str) -> Comment:
        # Business logic to add a comment to a post
        comment = self.comment_service.add_comment(content, user_id, post_id)
        return comment
