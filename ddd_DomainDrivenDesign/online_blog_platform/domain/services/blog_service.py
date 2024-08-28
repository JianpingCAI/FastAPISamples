from typing import Optional
from domain.models.blog import Blog
from domain.models.user import User
from domain.repositories.blog_repository import BlogRepository


class BlogService:
    def __init__(self, blog_repository: BlogRepository):
        self.blog_repository = blog_repository

    def create_blog(self, title: str, description: str, user: User) -> Blog:
        blog = Blog(title=title, description=description, user=user)
        self.blog_repository.save(blog)
        return blog

    def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        return self.blog_repository.find_by_id(blog_id)

    def add_post_to_blog(self, blog: Blog, post: "Post") -> None:
        blog.add_post(post)
        self.blog_repository.save(blog)
