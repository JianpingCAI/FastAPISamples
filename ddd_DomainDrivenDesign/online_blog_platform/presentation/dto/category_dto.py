from pydantic import BaseModel


class CategoryDTO(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
