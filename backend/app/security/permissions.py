from fastapi import HTTPException
from app.models.role import UserRole
from app.models.user import User


def ensure_role(user: User, allowed_roles: tuple[UserRole, ...]) -> None:
    if user.role not in allowed_roles:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
