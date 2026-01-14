from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum

class UserRole(str, Enum):
    admin = "admin"
    regular = "regular"


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    avatar: Optional[str] = None
    role: UserRole = Field(default=UserRole.regular)
    posts: List["Post"] = Relationship(back_populates="user")