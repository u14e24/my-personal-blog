from sqlmodel import SQLModel, create_engine, Session
from models.post import Post
from models.post_tag import PostTag
from models.tag import Tag

DATABASE_URL = "sqlite:///./blog_zsoptij.db"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session
