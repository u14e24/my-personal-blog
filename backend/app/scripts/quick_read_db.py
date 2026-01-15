import sqlite3
from sqlmodel import Session, select
from app.database import engine
from app.models.post import Post
from app.models.user import User
from app.models.tag import Tag
from app.models.post_tag import PostTag


with Session(engine) as session:
    posts = session.exec(select(Post)).all()    
    users = session.exec(select(User)).all()
    tag_table = session.exec(select(Tag)).all()
    post_tag = session.exec(select(PostTag)).all()

print(f"POSTS TABLE: {posts}")
print(f"USERS TABLE: {users}")
print(f"TAG TABLE: {tag_table}")
print(f"POST TAG: {post_tag}")
