from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.utils.security import get_current_user, get_current_admin
from app.services.post_service import create_post, get_posts, delete_posts as service_delete_posts, update_post
from app.schemas.post_schema import PostCreate, PostRead, PostDelete, PostUpdate
from app.database import get_session
from pydantic import BaseModel
from app.models.post import Post
from app.models.user import User
import re
router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead)
def add_post(post: PostCreate,
             session: Session = Depends(get_session),
             current_user: User = Depends(get_current_user),
    ):
    return create_post(post, current_user, session)
    

@router.get("/", response_model=list[PostRead])
def read_posts(tag: str | None = None, 
               skip: int = Query(0, ge=0), 
               limit: int = Query(10, ge=1, le=100), 
               session: Session = Depends(get_session)):
    
    posts = get_posts(session, skip, limit, tag)
    return [PostRead.model_validate(post) for post in posts]


@router.get("/{slug}", response_model=PostRead)
def get_post_by_slug(slug: str, session: Session = Depends(get_session)):
    # Parse slug to extract post ID (assumed to be at the end after the last '-')
    parts = slug.rsplit('-', 1)
    if len(parts) != 2 or not parts[1].isdigit():
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_id = int(parts[1])
    
    post = session.exec(
        select(Post)
        .where(Post.id == post_id)
        .options(selectinload(Post.user), selectinload(Post.tags))
    ).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    return PostRead.model_validate(post)


@router.delete("/")
def delete_posts(
    payload: PostDelete,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    deleted = service_delete_posts(session, payload.post_ids, current_user)

    if deleted == 0:
        raise HTTPException(
            status_code=403,
            detail="No posts deleted (not found or not authorized)",
        )

    return {"deleted": deleted}


@router.put("/{post_id}", response_model=PostRead)
def update_post_route(
    post_id: int,
    update_data: PostUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    return update_post(post_id, update_data, current_user, session)
