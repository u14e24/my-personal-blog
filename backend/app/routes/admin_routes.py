from fastapi import APIRouter, Depends
from datetime import datetime, timedelta
import app.utils.security as security
from app.schemas.user_schema import OpenUserCreationWindow

admin_router = APIRouter(prefix="/admin", tags=["Admin"])


@admin_router.post("/open-user-creation")
def open_user_creation(
    request: OpenUserCreationWindow,
    _ : object = Depends(security.get_current_admin),
):
    """Open a window for user creation (admin only).

    This sets module-level variables on `app.utils.security` so other
    parts of the app can consult them.
    """
    # assign directly on the security module (don't use Python `global` with attributes)
    security.USER_CREATION_OPEN_UNTIL = datetime.utcnow() + timedelta(minutes=request.minutes)
    security.CURRENT_INVITE_CODE = request.invite_code
    security.USER_CREATED_THIS_WINDOW = False

    return {
        "open_until": security.USER_CREATION_OPEN_UNTIL.isoformat(),
        "minutes": request.minutes,
        "invite_code": security.CURRENT_INVITE_CODE,
    }
