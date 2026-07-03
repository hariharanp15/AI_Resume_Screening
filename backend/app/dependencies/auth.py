from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.models.user import User
from app.security.jwt import decode_access_token
from app.security.oauth2 import oauth2_scheme


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_error
    except JWTError as exc:
        raise credentials_error from exc
    user = db.get(User, int(user_id))
    if not user or not user.is_active:
        raise credentials_error
    return user
