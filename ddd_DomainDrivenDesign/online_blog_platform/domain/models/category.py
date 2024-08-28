from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Category:
    id: Optional[int] = None
    name: str = field(default_factory=str)
