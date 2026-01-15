from pydantic import BaseModel
from app.schemas.user_schema import UserPublic
from app.schemas.tag_schema import TagRead
from app.models.user import User
from fastapi import Depends


class PostCreate(BaseModel):
    title: str
    current_user: User
    content: str
    tags: list[str]

class PostRead(BaseModel):
    title: str
    content: str
    user: UserPublic
    tags: list[TagRead]
    
    class Config:
        from_attributes = True
