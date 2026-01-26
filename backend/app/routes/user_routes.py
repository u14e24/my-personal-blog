from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.schemas.user_schema import UserCreate, UserPublic
from app.database import get_session
from pydantic import BaseModel
from app.models.user import User, UserRole
from app.models.post import Post
from app.services.user_service import delete_user_and_posts
from fastapi.security import OAuth2PasswordRequestForm
import app.utils.security as security
from datetime import datetime

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/", response_model=UserPublic)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_session), #database session
):
    # If invite system is active, validate invite code provided in JSON body
    if getattr(security, "CURRENT_INVITE_CODE", None) is not None:
        security.ensure_user_creation_allowed(getattr(user, "invite_code", None))
    existing = session.exec(
        select(User).where(User.username == user.username)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = User(
        username=user.username,
        hashed_password=security.hash_passwd(user.password),
        avatar=user.avatar,
        role=UserRole.regular,  # enforced
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    # mark that a user was created in this window (if invite system active)
    if getattr(security, "CURRENT_INVITE_CODE", None) is not None:
        security.USER_CREATED_THIS_WINDOW = True
    
    return db_user


@users_router.get("/", response_model=list[UserPublic])
def show_users(
    _ : User = Depends(security.get_current_admin),
    session: Session = Depends(get_session),
):
    """Return all users (admin only)."""
    users = session.exec(select(User)).all()
    return [UserPublic.model_validate(u) for u in users]


@users_router.delete("/{user_id}")
def delete_user(
    user_id: int,
    _ : User = Depends(security.get_current_admin),
    session: Session = Depends(get_session),
):
    """Hard-delete a user and all their posts (admin only)."""
    deleted_posts, deleted_users = delete_user_and_posts(session, user_id)

    if deleted_users == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"deleted_user_id": user_id, "deleted_posts": deleted_posts}


auth_router = APIRouter(tags=["auth"])
@auth_router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session)
):
    user = session.exec(
        select(User).where(User.username == form_data.username)
    ).first()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = security.create_access_token({"sub": str(user.username)})

    return {"access_token": token, "token_type": "bearer"}

@users_router.get("/me")
def me(current_user: User = Depends(security.oauth2_scheme)):
    return {
        "current_user": current_user
    }
