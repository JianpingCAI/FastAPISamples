from dataclasses import dataclass, field
from typing import List, Optional
from domain.models.comment import Comment
from domain.models.category import Category
from domain.models.tag import Tag


@dataclass
class Post:
    id: Optional[int] = None
    title: str = field(default_factory=str)
    content: str = field(default_factory=str)

    blog_id: Optional[int] = None  # Store Blog ID instead of direct reference
    comments: List[Comment] = field(default_factory=list)  # Aggregates Comments
    categories: List[Category] = field(default_factory=list)
    tags: List[Tag] = field(default_factory=list)

    def add_comment(self, comment: Comment):
        self.comments.append(comment)

    def add_category(self, category: Category):
        self.categories.append(category)

    def add_tag(self, tag: Tag):
        self.tags.append(tag)
