#from sqlmodel import select
#from database import get_session
#from models.post import Post

#def create_post(post_data, session):
#    post = Post(**post_data.dict())
#    session.add(post)
#    session.commit()
#    session.refresh(post)
#    return post

#def get_posts(session):
#    return session.exec(select(Post)).all()
