from dataclasses import dataclass, field
from typing import List, Optional
from domain.models.post import Post

@dataclass
class Blog:
    id: Optional[int] = None
    title: str = field(default_factory=str)
    description: str = field(default_factory=str)
    
    user_id: Optional[int] = None  # Store User ID instead of direct reference
    posts: List[Post] = field(default_factory=list)  # Aggregates Posts
    
    def add_post(self, post: Post):
        self.posts.append(post)
    
    def remove_post(self, post: Post):
        self.posts.remove(post)
