from datetime import datetime
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    required_skills: list[str] = []
    experience_requirement: str
    location: str
    employment_type: str
    content: str


class JobCreate(JobBase):
    pass


class JobUpdate(JobBase):
    pass


class JobRead(JobBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
