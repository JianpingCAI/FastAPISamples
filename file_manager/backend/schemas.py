from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class NodeDataBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_folder: bool = False
    file_path: Optional[str] = None
    parent_id: Optional[str] = None


class NodeDataCreate(NodeDataBase):
    pass


class NodeDataUpdate(BaseModel):
    name: Optional[str] = None
    is_folder: Optional[bool] = None
    description: Optional[str] = None


class NodeDataORM(NodeDataBase):
    id: str

    model_config = ConfigDict(from_attributes=True)


class FileMetadata(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: str
