from sqlmodel import Session, select, delete
from app.models.user import User
from app.models.post import Post
from fastapi import HTTPException
from app.utils.security import hash_passwd


def delete_user_and_posts(session: Session, user_id: int) -> tuple[int, int]:
    """Delete all posts for a user and then delete the user itself.

    Returns a tuple (deleted_posts_count, deleted_users_count).
    If the user does not exist returns (0, 0).
    """
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        return 0, 0

    post_result = session.exec(delete(Post).where(Post.user_id == user_id))
    user_result = session.exec(delete(User).where(User.id == user_id))

    session.commit()

    return post_result.rowcount or 0, user_result.rowcount or 0


def update_user(session: Session, user_id: int, update_data):
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if update_data.username is not None:
        # Check if username is already taken
        existing = session.exec(select(User).where(User.username == update_data.username)).first()
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = update_data.username
    
    if update_data.password is not None:
        user.hashed_password = hash_passwd(update_data.password)
    
    if update_data.avatar is not None:
        user.avatar = update_data.avatar
    
    session.commit()
    session.refresh(user)
    return user
