from typing import List
from sqlmodel import SQLModel, Field, Relationship

from .post_tag import PostTag

class Post(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    content: str
    tags: List["Tag"] = Relationship(
        #back_populates="",
        link_model = PostTag
    )
