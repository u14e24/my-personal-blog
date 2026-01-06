from sqlmodel import select
from database import get_session
from models.post import Post
from models.tag import Tag

def create_post(post_data, session):
    post = Post(**post_data.dict())
    
    tag_objs = []
    for tag_name in post_data.tags:  
        tag = session.query(Tag).filter_by(name=tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
            session.commit()
            session.refresh(tag)
        
        tag_objs.append(tag)
    post = Post(title=post_data.title, content=post_data.content, tags=tag_objs)
    
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_posts(session):
    return session.exec(select(Post)).all()
