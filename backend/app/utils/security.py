from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Header
from app.database import get_session
from sqlmodel import Session, select 
from app.models.user import User, UserRole

# TODO: Move SECRET_KEY to environment variables
SECRET_KEY = "63f4945d921d599f27ae4fdf5bada3f1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


USER_CREATION_OPEN_UNTIL = None
CURRENT_INVITE_CODE: str | None = None
USER_CREATION_OPEN_UNTIL: datetime | None = None

USER_CREATED_THIS_WINDOW = False


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_passwd(password: str) -> str:
    # TODO: Add password strength validation (e.g., require uppercase, numbers) before hashing
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401)
    except JWTError:
        raise HTTPException(status_code=401)

    user = session.exec(
        select(User).where(User.username == username)
    ).first()
    
    if not user:
        raise HTTPException(status_code=401)

    return user

def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


def user_creation_allowed(
    invite_code: str = Header(..., alias="X-Invite-Code")
):
    return ensure_user_creation_allowed(invite_code)


def ensure_user_creation_allowed(invite_code: str | None):
    """Validate invite code and window. Raises HTTPException on failure.

    This helper can be called from routes (passing invite_code from JSON)
    or used as a dependency via `user_creation_allowed` which reads from
    the `X-Invite-Code` header.
    """
    # Check invite code
    if CURRENT_INVITE_CODE is None or invite_code != CURRENT_INVITE_CODE:
        raise HTTPException(
            status_code=403,
            detail="Invalid invite code"
        )

    # Check window
    if USER_CREATION_OPEN_UNTIL is None:
        raise HTTPException(
            status_code=403,
            detail="User creation is currently closed"
        )

    if datetime.utcnow() > USER_CREATION_OPEN_UNTIL:
        raise HTTPException(
            status_code=403,
            detail="User creation window expired"
        )

    # Optional: only allow one user per window
    if USER_CREATED_THIS_WINDOW:
        raise HTTPException(
            status_code=403,
            detail="User already created during this window"
        )
