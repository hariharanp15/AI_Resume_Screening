from datetime import datetime
from pydantic import BaseModel, EmailStr


class CandidateBase(BaseModel):
    name: str
    email: EmailStr | None = None
    phone: str | None = None
    skills: list[str] = []
    work_experience: str | None = None
    education: str | None = None


class CandidateUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None


class CandidateRead(CandidateBase):
    id: int
    resume_file_path: str
    created_at: datetime

    class Config:
        from_attributes = True


class CandidateDetail(CandidateRead):
    resume_text: str
