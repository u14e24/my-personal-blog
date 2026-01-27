from sqlmodel import select, delete
from app.database import get_session
from sqlalchemy.orm import selectinload
from app.models.post import Post
from app.models.tag import Tag
from app.models.post_tag import PostTag
from fastapi import HTTPException

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

def update_post(post_id, update_data, current_user, session):
    """
    Update a post. Admins can update any post, users can update only their own posts.
    """
    post = session.exec(select(Post).where(Post.id == post_id)).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if current_user.role != "admin" and post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    if update_data.title is not None:
        post.title = update_data.title
    if update_data.content is not None:
        post.content = update_data.content
    if update_data.cover_image is not None:
        post.cover_image = update_data.cover_image
    
    if update_data.tags is not None:
        # Clear existing tags
        session.exec(delete(PostTag).where(PostTag.post_id == post_id))
        # Add new tags
        tag_objs = []
        for tag_name in update_data.tags:
            tag = session.exec(select(Tag).where(Tag.name == tag_name)).first()
            if not tag:
                tag = Tag(name=tag_name)
                session.add(tag)
            tag_objs.append(tag)
        post.tags = tag_objs
    
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


def delete_posts(session, post_ids, current_user):
    """
    Admin: deletes any post
    User: deletes only their own posts
    Returns number of deleted posts
    """

    stmt = delete(Post).where(Post.id.in_(post_ids))

    # Non-admins can delete only their own posts
    if current_user.role != "admin":
        stmt = stmt.where(Post.user_id == current_user.id)

    result = session.exec(stmt)
    session.commit()

    return result.rowcount or 0

