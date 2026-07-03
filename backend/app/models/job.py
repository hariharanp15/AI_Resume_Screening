from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class JobDescription(Base):
    __tablename__ = "job_descriptions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    required_skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    experience_requirement: Mapped[str] = mapped_column(String(255))
    location: Mapped[str] = mapped_column(String(255))
    employment_type: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_by_user = relationship("User", back_populates="jobs")
    evaluations = relationship("Evaluation", back_populates="job")
