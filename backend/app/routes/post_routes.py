from fastapi import APIRouter, Depends
from sqlmodel import Session, select 
from services.post_service import create_post, get_posts
from schemas.post_schema import PostCreate, PostRead
from database import get_session
from pydantic import BaseModel
from models.post import Post

router = APIRouter(prefix="/posts", tags=["Posts"])

@router.post("/", response_model=PostRead)
def add_post(post: PostCreate, session: Session = Depends(get_session)):
    return create_post(post, session)


@router.get("/", response_model=list[PostRead])
def read_posts(tag: str | None = None, session: Session = Depends(get_session)):

    if tag:
        statement = statement.where(Post.tags == tag)

    print ("Tag: ", tag)
    print ("post tag: ", Post.tags)
    posts = session.exec(select(Post)).all() 
    posts_conv = [PostRead.from_orm(p) for p in posts]
    return posts_conv
