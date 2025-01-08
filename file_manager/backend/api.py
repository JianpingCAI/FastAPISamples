from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from backend.crud import (
    get_all,
    get_by_id,
    create,
    update,
    get_all_files,
    get_all_folders,
    delete_with_descendants,
)
from backend.schemas import (
    NodeDataORM,
    NodeDataCreate,
    NodeDataUpdate,
    FileMetadata,
)
from backend.database import get_db
import json
import os
import uuid
from pathlib import Path

router = APIRouter()

# Add configuration for file storage
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# Handle file downloads
@router.get("/download/{file_id}", response_class=FileResponse)
async def download_file(file_id: str, db: Session = Depends(get_db)) -> FileResponse:
    file_node: Optional[NodeDataORM] = get_by_id(db, file_id)
    if not file_node or file_node.is_folder or not file_node.file_path:
        raise HTTPException(status_code=404, detail="File not found")

    if not os.path.exists(file_node.file_path):
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(file_node.file_path, filename=file_node.name, media_type="application/octet-stream")


@router.get("/reference_data/root", response_model=List[NodeDataORM])
async def read_root_nodes(db: Session = Depends(get_db)) -> List[NodeDataORM]:
    """Get all root reference data nodes."""
    return get_all(db, parent_id=None)


@router.get("/reference_data/parent/{parent_id}", response_model=List[NodeDataORM])
async def read_by_parent_id(parent_id: str, db: Session = Depends(get_db)) -> List[NodeDataORM]:
    """Get all reference data nodes for a specified parent ID."""
    return get_all(db, parent_id=parent_id)


@router.get("/folders/parent/{parent_id}", response_model=List[NodeDataORM])
async def read_folders_by_parent_id(parent_id: str, db: Session = Depends(get_db)) -> List[NodeDataORM]:
    """Get all reference data nodes for a specified parent ID."""
    return get_all_folders(db, parent_id=parent_id)


@router.get("/files/parent/{parent_id}", response_model=List[NodeDataORM])
async def read_files_by_parent_id(parent_id: str, db: Session = Depends(get_db)) -> List[NodeDataORM]:
    """Get all reference data nodes for a specified parent ID."""
    return get_all_files(db, parent_id=parent_id)


@router.get("/reference_data/{data_id}", response_model=NodeDataORM)
async def read_by_id(data_id: str, db: Session = Depends(get_db)) -> NodeDataORM:
    """Get a reference data entry by ID."""
    data: Optional[NodeDataORM] = get_by_id(db, data_id)
    if not data:
        raise HTTPException(status_code=404, detail="Reference data not found")
    return data


@router.get("/reference_data/", response_model=List[NodeDataORM])
async def read_all(parent_id: Optional[str] = None, db: Session = Depends(get_db)) -> List[NodeDataORM]:
    """Get all reference data for a given parent."""
    return get_all(db, parent_id)


@router.post("/reference_data/", response_model=NodeDataORM)
async def create_data(data: NodeDataCreate, db: Session = Depends(get_db)) -> NodeDataORM:
    """Create a new reference data entry."""
    if data.parent_id:
        parent: Optional[NodeDataORM] = get_by_id(db, data.parent_id)
        if not parent:
            raise HTTPException(status_code=404, detail="Parent node not found")
        if not parent.is_folder:
            raise HTTPException(status_code=400, detail="Parent must be a folder")

    return create(db, data)


@router.put("/reference_data/{data_id}", response_model=NodeDataORM)
async def update_data(data_id: str, data: NodeDataUpdate, db: Session = Depends(get_db)) -> NodeDataORM:
    """Update a reference data entry."""
    return update(db, data_id, data)


@router.delete("/reference_data/{data_id}")
async def delete_data(data_id: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """Delete a reference data entry and all its children."""
    try:
        result = delete_with_descendants(db, data_id)
        if result["status"] == "error":
            raise HTTPException(status_code=404, detail=result["message"])
        return result

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting node: {str(e)}")


@router.post("/upload", response_model=NodeDataORM)
async def upload_file(
    file: UploadFile = File(...),
    metadata: str = Form(...),
    db: Session = Depends(get_db),
) -> NodeDataORM:
    """Upload a file with metadata."""
    try:
        metadata_dict: Dict[str, Any] = json.loads(metadata)
        metadata_obj: FileMetadata = FileMetadata(**metadata_dict)

        if metadata_obj.parent_id:
            parent: Optional[NodeDataORM] = get_by_id(db, metadata_obj.parent_id)
            if not parent:
                raise HTTPException(status_code=404, detail="Parent folder not found")
            if not parent.is_folder:
                raise HTTPException(status_code=400, detail="Parent must be a folder")

        # Generate unique filename to avoid collisions
        file_ext: str = os.path.splitext(metadata_obj.name)[1]
        unique_filename: str = f"{uuid.uuid4()}{file_ext}"
        file_path: Path = UPLOAD_DIR / unique_filename

        # Save file content
        with open(file_path, "wb") as f:
            file_content = file.file.read()
            f.write(file_content)

        # Create reference data entry
        new_data: NodeDataCreate = NodeDataCreate(
            name=metadata_obj.name,
            is_folder=False,
            description=metadata_obj.description,
            file_path=str(file_path),
            parent_id=metadata_obj.parent_id,
        )
        return create(db, new_data)

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid metadata format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
