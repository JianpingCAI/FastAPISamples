from typing import Optional, List, Union, Dict, Any
from sqlalchemy.orm import Session
from backend.models import NodeDataORM
from backend.schemas import NodeDataCreate, NodeDataUpdate
import os


def get_all(db: Session, parent_id: Optional[str] = None) -> List[NodeDataORM]:
    """Retrieve all nodes under a given parent."""
    return db.query(NodeDataORM).filter(NodeDataORM.parent_id == parent_id).all()


def get_all_files(db: Session, parent_id: Optional[str] = None) -> List[NodeDataORM]:
    """Retrieve all files under a given parent."""
    return db.query(NodeDataORM).filter(NodeDataORM.parent_id == parent_id, NodeDataORM.is_folder == False).all()


def get_all_folders(db: Session, parent_id: Optional[str] = None) -> List[NodeDataORM]:
    """Retrieve all folders under a given parent."""
    return db.query(NodeDataORM).filter(NodeDataORM.parent_id == parent_id, NodeDataORM.is_folder == True).all()


def get_by_id(db: Session, id: str) -> Union[NodeDataORM, None]:
    """Retrieve a node by its ID."""
    return db.query(NodeDataORM).filter(NodeDataORM.id == id).first()


def create(db: Session, data: NodeDataCreate) -> NodeDataORM:
    """Create a new reference data entry."""
    new_data = NodeDataORM(**data.model_dump())
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


def update(db: Session, id: str, data: NodeDataUpdate) -> Union[NodeDataORM, None]:
    """Update an existing reference data entry."""
    ref_data = db.query(NodeDataORM).filter(NodeDataORM.id == id).first()
    for key, value in data.dict(exclude_unset=True).items():
        setattr(ref_data, key, value)
    db.commit()
    db.refresh(ref_data)
    return ref_data


def collect_file_paths(node: NodeDataORM) -> List[str]:
    """Recursively collect all file paths from a node and its descendants."""
    paths = []
    if not node.is_folder and node.file_path:
        paths.append(node.file_path)
    for child in node.children:
        paths.extend(collect_file_paths(child))
    return paths


# TODO: not working yet, due to ForeignKey constraint
def delete_with_descendants(db: Session, node_id: str) -> Dict[str, Any]:
    """Delete a node and all its descendants, including associated files."""
    try:
        node = db.query(NodeDataORM).get(node_id)
        if not node:
            return {"status": "error", "message": "Node not found"}

        # Collect file paths before deletion
        file_paths = collect_file_paths(node)

        # Delete node (SQLAlchemy cascade will handle descendants)
        db.delete(node)
        db.commit()

        # Clean up files after successful database deletion
        deleted_files = 0
        failed_files = 0
        for path in file_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                    deleted_files += 1
                except OSError as e:
                    failed_files += 1
                    print(f"Error deleting file {path}: {e}")

        return {"status": "success", "message": f"Node deleted with {deleted_files} files", "failed_deletes": failed_files}

    except Exception as e:
        db.rollback()
        raise e
