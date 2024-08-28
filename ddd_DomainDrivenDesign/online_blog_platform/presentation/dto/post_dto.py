from pydantic import BaseModel
from typing import List, Optional


class PostCreateDTO(BaseModel):
    title: str
    content: str


class PostResponseDTO(BaseModel):
    id: int
    title: str
    content: str

    blog_id: int
    comments: Optional[List[int]]  # List of comment IDs

    class Config:
        from_attributes = True
