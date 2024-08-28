from typing import List
from sqlalchemy.orm import Session
from domain.models.post import Post
from domain.services.search_service import SearchService

class SearchManager:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.search_service = SearchService(db_session)

    def search_posts_by_keyword(self, keyword: str) -> List[Post]:
        # Business logic to search posts by keyword
        posts = self.search_service.search_posts_by_keyword(keyword)
        return posts

    def search_posts_by_category(self, category_name: str) -> List[Post]:
        # Business logic to search posts by category
        posts = self.search_service.search_posts_by_category(category_name)
        return posts

    def search_posts_by_tag(self, tag_name: str) -> List[Post]:
        # Business logic to search posts by tag
        posts = self.search_service.search_posts_by_tag(tag_name)
        return posts
