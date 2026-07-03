from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base


class Summary(Base):
    __tablename__ = "summaries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    evaluation_id: Mapped[int] = mapped_column(ForeignKey("evaluations.id", ondelete="CASCADE"))
    overview: Mapped[str] = mapped_column(Text)
    skill_assessment: Mapped[str] = mapped_column(Text)
    experience_summary: Mapped[str] = mapped_column(Text)
    hiring_recommendation: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    evaluation = relationship("Evaluation", back_populates="summaries")
