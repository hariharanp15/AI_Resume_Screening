from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserUpdate


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.full_name.asc()).all()


def update_profile(db: Session, user: User, payload: UserUpdate) -> User:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user
