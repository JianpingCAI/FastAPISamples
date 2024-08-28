from pydantic import BaseModel
from typing import List, Optional


class BlogCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None


class BlogResponseDTO(BaseModel):
    id: int
    title: str
    description: Optional[str]

    user_id: int
    posts: Optional[List[int]]  # List of post IDs

    class Config:
        from_attributes = True
