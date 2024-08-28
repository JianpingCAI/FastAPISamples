from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.services.blog_service import BlogService
from infrastructure.database import get_db
from presentation.dto.blog_dto import BlogCreateDTO, BlogResponseDTO

router = APIRouter()


@router.post("/blogs/", response_model=BlogResponseDTO)
def create_blog(blog_dto: BlogCreateDTO, db: Session = Depends(get_db)):
    blog_service = BlogService(db)
    blog = blog_service.create_blog(blog_dto.title, blog_dto.description, user_id)
    return blog


@router.get("/blogs/{blog_id}", response_model=BlogResponseDTO)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog_service = BlogService(db)
    blog = blog_service.get_blog_by_id(blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
