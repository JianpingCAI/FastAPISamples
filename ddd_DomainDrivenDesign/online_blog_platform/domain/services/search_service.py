from typing import List
from domain.models.post import Post
from domain.repositories.post_repository import PostRepository


class SearchService:
    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def search_posts_by_keyword(self, keyword: str) -> List[Post]:
        return self.post_repository.search_by_keyword(keyword)

    def search_posts_by_category(self, category_name: str) -> List[Post]:
        return self.post_repository.find_by_category(category_name)

    def search_posts_by_tag(self, tag_name: str) -> List[Post]:
        return self.post_repository.find_by_tag(tag_name)
