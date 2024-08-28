from pydantic import BaseModel


class TagDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
