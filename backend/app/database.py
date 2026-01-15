from sqlmodel import SQLModel, create_engine, Session
from app.models.post import Post
from app.models.post_tag import PostTag
from app.models.tag import Tag
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

DATABASE_URL = f"sqlite:///{BASE_DIR}/blog_zsoptij.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def get_engine():
    return engine