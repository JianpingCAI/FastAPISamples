from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Comment:
    id: Optional[int] = None
    content: str = field(default_factory=str)
    
    post_id: Optional[int] = None  # Store Post ID instead of direct reference
    user_id: Optional[int] = None  # Store User ID instead of direct reference
