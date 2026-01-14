from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select 
from schemas.user_schema import UserCreate, UserPublic
from database import get_session
from pydantic import BaseModel
from models.user import User, UserRole
from fastapi.security import OAuth2PasswordRequestForm
import utils.security as security

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/", response_model=UserPublic)
def create_user(
    user: UserCreate,
    admin: User = Depends(security.get_current_admin),
    session: Session = Depends(get_session), #database session
):
    
    
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

    return db_user

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