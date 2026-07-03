from pydantic import BaseModel
from app.models.role import UserRole


class RoleRead(BaseModel):
    name: UserRole
