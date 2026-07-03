from pydantic import BaseModel
from app.models.role import UserRole


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: UserRole
    full_name: str
