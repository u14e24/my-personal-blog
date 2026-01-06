from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str
    tags: list[str]
    
    class Config:
        orm_mode = True 

    @classmethod
    def from_orm(cls, post: "Post"):
        return cls(
            id=post.id,
            title=post.title,
            content=post.content,
            tags=[tag.name for tag in post.tags] 
        )


class PostRead(PostCreate):
    title: str
    content: str
    tags: list[str]

    @classmethod
    def from_orm(cls, post: "Post"):
        return cls(
            title=post.title,
            content=post.content,
            tags=[tag.name for tag in post.tags] 
        )

    