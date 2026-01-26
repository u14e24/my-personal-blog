import sqlite3
from sqlmodel import Session, select
from sqlalchemy import delete
from app.database import engine
#from app.models.post import Post
#from app.models.user import User
#from app.models.tag import Tag
from app.models.post_tag import PostTag


with Session(engine) as session:
    session.exec(
        delete(PostTag).where(PostTag.tag_id == 4)
    )
    session.commit()
print("DONE")