from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.services.tag_service import TagService
from infrastructure.database import get_db
from presentation.dto.tag_dto import TagDTO

router = APIRouter()


@router.post("/tags/", response_model=TagDTO)
def create_tag(tag_dto: TagDTO, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    tag = tag_service.create_tag(tag_dto.name)
    return TagDTO.from_orm(tag)


@router.get("/tags/{tag_id}", response_model=TagDTO)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag_service = TagService(db)
    tag = tag_service.get_tag_by_id(tag_id)
    if tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagDTO.from_orm(tag)
