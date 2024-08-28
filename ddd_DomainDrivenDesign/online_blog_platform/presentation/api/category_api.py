from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.services.category_service import CategoryService
from infrastructure.database import get_db
from presentation.dto.category_dto import CategoryDTO

router = APIRouter()


@router.post("/categories/", response_model=CategoryDTO)
def create_category(category_dto: CategoryDTO, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    category = category_service.create_category(category_dto.name)
    return CategoryDTO.from_orm(category)


@router.get("/categories/{category_id}", response_model=CategoryDTO)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category_service = CategoryService(db)
    category = category_service.get_category_by_id(category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return CategoryDTO.from_orm(category)
