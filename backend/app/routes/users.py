from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.role import UserRole
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate
from app.services.user_service import list_users, update_profile


router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserRead])
def users(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    return list_users(db)


@router.get("/me", response_model=UserRead)
def me(user: User = Depends(get_current_user)):
    return user


@router.put("/me", response_model=UserRead)
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return update_profile(db, user, payload)
