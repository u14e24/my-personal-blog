from sqlmodel import select
from app.database import get_session
from sqlalchemy.orm import selectinload
from app.models.post import Post
from app.models.tag import Tag

def create_post(post_data, current_user, session):
    tag_objs = []
    for tag_name in post_data.tags:  
        tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
        if not tag:
            tag = Tag(name=tag_name)
            session.add(tag)
        tag_objs.append(tag)


    post = Post(
        title=post_data.title,
        user_id = current_user.id,
        content=post_data.content,
        cover_image = post_data.cover_image,
        tags=tag_objs
    )
    
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return post

def get_posts(session, skip, limit, tag):
    statement = select(Post).options(
        selectinload(Post.user),
        selectinload(Post.tags),
    )
    
    if tag:
        statement = (
            statement
            .join(Post.tags)
            .where(Tag.name == tag)
            .distinct()
        )

    statement = statement.offset(skip).limit(limit)

    posts = session.exec(statement).all()
    
    return posts


def delete_post(session, post_id: int, current_user) -> bool:
    post = session.get(Post, post_id)
    if not post:
        return False  # Post does not exist
    
    # Check ownership or admin role
    if post.user_id != current_user.id and current_user.role != "admin":
        return False  # Unauthorized
    
    session.delete(post)
    session.commit()
    return True