from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.services.auth_service import authenticate_user, register_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return register_user(db, payload)


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, db: Session = Depends(get_db)):
    content_type = request.headers.get("content-type", "")
    if "application/x-www-form-urlencoded" in content_type:
        form = await request.form()
        email = str(form.get("username") or form.get("email") or "")
        password = str(form.get("password") or "")
    else:
        payload = LoginRequest.model_validate(await request.json())
        email = payload.email
        password = payload.password
    return authenticate_user(db, email, password)
