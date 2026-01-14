from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from .user import User
from .post_tag import PostTag

class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship (back_populates="posts")
    tags: List["Tag"] = Relationship(
        back_populates="posts",
        link_model = PostTag
    )
