from pydantic import BaseModel, Field, model_validator, field_validator, ValidationError
from app.schemas.user_schema import UserPublic
from app.schemas.tag_schema import TagRead
from app.models.user import User
from fastapi import Depends
import re

DEFAULT_COVER_IMAGE = "/static/images/default-post-cover.png"
# Regex for path ending with common image extensions
IMAGE_PATH_REGEX = re.compile(r"^.*\.(jpg|jpeg|png|webp)$", re.IGNORECASE)

class PostDelete(BaseModel):
    post_ids: list[int] = Field(min_length=1)


class PostBase(BaseModel):
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None
    cover_image: str | None = None
    
    @field_validator("cover_image", mode="before")
    def validate_cover_image(cls, v):
        if v is not None and not IMAGE_PATH_REGEX.match(v):
            raise ValueError("cover_image must be a valid path ending in .jpg, .jpeg, .png, or .webp")
        return v


class PostCreate(PostBase):
    title: str
    content: str
    tags: list[str]


class PostUpdate(PostBase):
    pass


class PostRead(BaseModel):
    title: str
    content: str
    user: UserPublic
    tags: list[TagRead]
    cover_image: str | None = None
    
    @model_validator(mode="before")
    def set_default_cover(self):
        if self.cover_image is None:
            self.cover_image = DEFAULT_COVER_IMAGE
        return self    
    
    class Config:
        from_attributes = True
