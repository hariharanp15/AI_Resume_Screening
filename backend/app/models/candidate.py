from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), index=True)
    email: Mapped[str | None] = mapped_column(String(255), index=True)
    phone: Mapped[str | None] = mapped_column(String(64))
    skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    work_experience: Mapped[str | None] = mapped_column(Text)
    education: Mapped[str | None] = mapped_column(Text)
    resume_text: Mapped[str] = mapped_column(Text)
    resume_file_path: Mapped[str] = mapped_column(String(512))
    embedding: Mapped[list[float]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    created_by_user = relationship("User", back_populates="candidates")
    evaluations = relationship("Evaluation", back_populates="candidate", cascade="all, delete-orphan")
    resumes = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
