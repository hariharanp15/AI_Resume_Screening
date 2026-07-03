from sqlalchemy import Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.config.database import Base
from app.models.role import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.RECRUITER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    candidates = relationship("Candidate", back_populates="created_by_user")
    jobs = relationship("JobDescription", back_populates="created_by_user")
    evaluations = relationship("Evaluation", back_populates="created_by_user")
