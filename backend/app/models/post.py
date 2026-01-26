from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from app.models.user import User
from app.models.post_tag import PostTag

class Post(SQLModel, table=True):
    __tablename__ = "post"
    __table_args__ = {"sqlite_autoincrement": True}
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")
    user: Optional[User] = Relationship (back_populates="posts")
    cover_image: str | None = Field(default=None) 
    tags: List["Tag"] = Relationship(
        back_populates="posts",
        link_model = PostTag
    )
