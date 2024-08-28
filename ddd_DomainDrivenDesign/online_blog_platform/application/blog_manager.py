from typing import Optional
from sqlalchemy.orm import Session
from domain.models.blog import Blog
from domain.models.post import Post
from domain.services.blog_service import BlogService
from domain.services.user_service import UserService

class BlogManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.blog_service = BlogService(db_session)
        self.user_service = UserService(db_session)

    def create_blog(self, user_id: int, title: str, description: str) -> Blog:
        # Ensure the user exists before creating a blog
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        # Business logic to create a blog
        blog = self.blog_service.create_blog(title, description, user.id)
        return blog

    def get_blog(self, blog_id: int) -> Optional[Blog]:
        # Business logic to retrieve a blog
        blog = self.blog_service.get_blog_by_id(blog_id)
        return blog

    def add_post_to_blog(self, blog_id: int, title: str, content: str) -> Post:
        # Ensure the blog exists before adding a post
        blog = self.get_blog(blog_id)
        if not blog:
            raise ValueError("Blog not found")

        # Business logic to add a post to a blog
        post = self.blog_service.add_post_to_blog(blog, title, content)
        return post
