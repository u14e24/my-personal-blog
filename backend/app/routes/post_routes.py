from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session 
from app.utils.security import get_current_user
from app.services.post_service import create_post, get_posts, delete_post
from app.schemas.post_schema import PostCreate, PostRead
from app.database import get_session
from pydantic import BaseModel
from app.models.post import Post
from app.models.user import User
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


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    success = delete_post(session, post_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete this post"
        )
    return None  # 204 No Content