from pydantic import BaseModel, Field, field_validator
from app.models.user import UserRole

class UserPublic(BaseModel):
    username: str
    avatar: str | None
    role: UserRole

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field (min_length=8, max_length=72)
    password: str
    avatar: str | None = None

    @field_validator("password")
    @classmethod
    def password_is_valid(cls, v: str):
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password too long (max 72 bytes)")
        return v