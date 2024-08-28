from dataclasses import dataclass, field
from typing import List, Optional

from domain.models.blog import Blog


@dataclass
class User:
    id: Optional[int] = None
    username: str = field(default_factory=str)
    email: str = field(default_factory=str)
    password: str = field(default_factory=str)
    
    blogs: List[Blog] = field(default_factory=list)

    def add_blog(self, blog: Blog):
        self.blogs.append(blog)

    def remove_blog(self, blog: Blog):
        self.blogs.remove(blog)
