from sqlalchemy import Column, ForeignKey

from sqlmodel import Field, SQLModel

class PostTag(SQLModel, table=True):
    post_id: int = Field(
        sa_column=Column(
            ForeignKey("post.id", ondelete="CASCADE"),
            primary_key=True
        )
    )
    tag_id: int = Field(
        sa_column=Column(
            ForeignKey("tag.id", ondelete="CASCADE"),
            primary_key=True
        )
    )