from typing import Optional
from domain.models.post import Post
from domain.models.blog import Blog
from domain.repositories.post_repository import PostRepository


class PostService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, title: str, content: str, blog: Blog) -> Post:
        post = Post(title=title, content=content, user=blog.user)
        blog.add_post(post)
        self.post_repository.save(post)
        return post

    def get_post_by_id(self, post_id: int) -> Optional[Post]:
        return self.post_repository.find_by_id(post_id)
