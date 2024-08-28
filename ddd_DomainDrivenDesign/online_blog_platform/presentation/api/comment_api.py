from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from domain.models.user import User
from domain.services.comment_service import CommentService
from infrastructure.database import get_db
from presentation.dto.comment_dto import CommentCreateDTO, CommentResponseDTO
from presentation.api.auth_api import get_current_user

router = APIRouter()


@router.post("/posts/{post_id}/comments/", response_model=CommentResponseDTO)
def add_comment(
    post_id: int,
    comment_dto: CommentCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    comment_service = CommentService(db)
    comment = comment_service.add_comment(
        content=comment_dto.content, user=current_user, post_id=post_id
    )
    return CommentResponseDTO.from_orm(comment)


@router.get("/posts/{post_id}/comments/", response_model=List[CommentResponseDTO])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    comments = comment_service.get_comments_for_post(post_id)
    return [CommentResponseDTO.from_orm(comment) for comment in comments]
