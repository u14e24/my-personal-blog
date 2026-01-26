from sqlmodel import Session, select, delete
from app.models.user import User
from app.models.post import Post


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
