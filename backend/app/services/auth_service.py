from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.auth import RegisterRequest
from app.security.hashing import hash_password, verify_password
from app.security.jwt import create_access_token


def register_user(db: Session, payload: RegisterRequest) -> dict:
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")
    user = User(
        email=payload.email,
        full_name=payload.full_name,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token(str(user.id), {"role": user.role.value})
    return {"access_token": token, "role": user.role, "full_name": user.full_name}


def authenticate_user(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(str(user.id), {"role": user.role.value})
    return {"access_token": token, "role": user.role, "full_name": user.full_name}
