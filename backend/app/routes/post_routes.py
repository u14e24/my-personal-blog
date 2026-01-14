from fastapi import APIRouter, Depends
from sqlmodel import Session 
from utils.security import get_current_user
from services.post_service import create_post, get_posts
from schemas.post_schema import PostCreate, PostRead
from database import get_session
from pydantic import BaseModel
from models.post import Post
from models.user import User
router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead)
def add_post(post: PostCreate,
             session: Session = Depends(get_session),
             current_user: User = Depends(get_current_user),
    ):
    return create_post(post, current_user, session)
    

@router.get("/", response_model=list[PostRead])
def read_posts(tag: str | None = None, session: Session = Depends(get_session)):
    
    return get_posts(session, tag)
    

