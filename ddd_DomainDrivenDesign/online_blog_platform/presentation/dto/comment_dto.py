from pydantic import BaseModel


class CommentCreateDTO(BaseModel):
    content: str
    post_id: int


class CommentResponseDTO(BaseModel):
    id: int
    content: str
    post_id: int
    user_id: int

    class Config:
        from_attributes = True
