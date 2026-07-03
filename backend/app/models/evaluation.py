from datetime import datetime
from sqlalchemy import DateTime, Float, ForeignKey, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id", ondelete="CASCADE"))
    job_id: Mapped[int | None] = mapped_column(ForeignKey("job_descriptions.id", ondelete="SET NULL"))
    match_score: Mapped[float | None] = mapped_column(Float)
    missing_skills: Mapped[list[str]] = mapped_column(JSON, default=list)
    strengths: Mapped[list[str]] = mapped_column(JSON, default=list)
    weaknesses: Mapped[list[str]] = mapped_column(JSON, default=list)
    summary: Mapped[str | None] = mapped_column(Text)
    interview_questions: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))

    candidate = relationship("Candidate", back_populates="evaluations")
    job = relationship("JobDescription", back_populates="evaluations")
    created_by_user = relationship("User", back_populates="evaluations")
    interviews = relationship("Interview", back_populates="evaluation", cascade="all, delete-orphan")
    summaries = relationship("Summary", back_populates="evaluation", cascade="all, delete-orphan")
