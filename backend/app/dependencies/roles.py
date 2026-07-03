from fastapi import Depends
from app.dependencies.auth import get_current_user
from app.models.role import UserRole
from app.models.user import User
from app.security.permissions import ensure_role


def require_roles(*roles: UserRole):
    def dependency(user: User = Depends(get_current_user)) -> User:
        ensure_role(user, roles)
        return user

    return dependency
