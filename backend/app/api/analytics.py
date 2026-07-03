from collections import Counter
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import require_roles
from app.models.candidate import Candidate
from app.models.evaluation import Evaluation
from app.models.job import JobDescription
from app.models.user import User, UserRole
from app.schemas.analytics import AnalyticsResponse


router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("", response_model=AnalyticsResponse)
def analytics(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    candidates = db.query(Candidate).all()
    jobs = db.query(JobDescription).all()
    scores = [score for (score,) in db.query(Evaluation.match_score).filter(Evaluation.match_score.isnot(None)).all()]
    skill_counts = Counter(skill for job in jobs for skill in job.required_skills)
    active_users = (
        db.query(User.full_name, func.count(Evaluation.id).label("count"))
        .join(Evaluation, Evaluation.created_by == User.id)
        .group_by(User.id)
        .order_by(func.count(Evaluation.id).desc())
        .limit(5)
        .all()
    )
    return AnalyticsResponse(
        total_candidates=len(candidates),
        total_job_descriptions=len(jobs),
        average_match_score=round(sum(scores) / len(scores), 2) if scores else 0.0,
        most_requested_skills=[{"skill": skill, "count": count} for skill, count in skill_counts.most_common(8)],
        recent_candidate_uploads=[{"id": c.id, "name": c.name, "created_at": c.created_at.isoformat()} for c in candidates[-5:]],
        most_active_users=[{"name": name, "evaluations": count} for name, count in active_users],
    )
