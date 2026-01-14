from sqlmodel import SQLModel, Field
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from .post_tag import PostTag

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)

    posts: List["Post"] = Relationship(back_populates="tags", link_model=PostTag)