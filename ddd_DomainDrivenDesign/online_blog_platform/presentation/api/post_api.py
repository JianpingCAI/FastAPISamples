from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from domain.services.post_service import PostService
from domain.services.comment_service import CommentService
from infrastructure.database import get_db
from presentation.dto.post_dto import PostCreateDTO, PostResponseDTO
from presentation.dto.comment_dto import CommentResponseDTO, CommentCreateDTO
from presentation.api.auth_api import get_current_user
from domain.models.user import User

router = APIRouter()


@router.post("/", response_model=PostResponseDTO)
def create_post(
    post_dto: PostCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_service = PostService(db)
    post = post_service.create_post(
        title=post_dto.title,
        content=post_dto.content,
        blog=current_user.blogs[
            0
        ],  # Assuming the user has one blog, otherwise, modify this logic
    )
    return PostResponseDTO.from_orm(post)


@router.get("/{post_id}", response_model=PostResponseDTO)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return PostResponseDTO.from_orm(post)


@router.get("/", response_model=List[PostResponseDTO])
def get_posts(db: Session = Depends(get_db)):
    post_service = PostService(db)
    posts = post_service.get_all_posts()
    return [PostResponseDTO.from_orm(post) for post in posts]


@router.put("/{post_id}", response_model=PostResponseDTO)
def update_post(
    post_id: int,
    post_dto: PostCreateDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if post is None or post.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    updated_post = post_service.update_post(
        post, title=post_dto.title, content=post_dto.content
    )
    return PostResponseDTO.from_orm(updated_post)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_service = PostService(db)
    post = post_service.get_post_by_id(post_id)
    if post is None or post.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Post not found or unauthorized")
    post_service.delete_post(post)
    return None


@router.post("/{post_id}/comments/", response_model=CommentResponseDTO)
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


@router.get("/{post_id}/comments/", response_model=List[CommentResponseDTO])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    comment_service = CommentService(db)
    comments = comment_service.get_comments_for_post(post_id)
    return [CommentResponseDTO.from_orm(comment) for comment in comments]
