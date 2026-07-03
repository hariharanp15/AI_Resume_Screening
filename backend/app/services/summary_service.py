from sqlalchemy.orm import Session
from app.ai.matcher import match_candidate_to_job
from app.ai.summary_generator import generate_candidate_summary
from app.models.evaluation import Evaluation
from app.models.summary import Summary
from app.models.user import User
from app.services.candidate_service import get_candidate_or_404
from app.services.job_service import get_job_or_404


def create_candidate_summary(db: Session, candidate_id: int, job_id: int | None, user: User) -> tuple[Evaluation, dict]:
    candidate = get_candidate_or_404(db, candidate_id)
    job = get_job_or_404(db, job_id) if job_id else None
    match = match_candidate_to_job(candidate, job) if job else None
    summary = generate_candidate_summary(candidate, job, match)
    evaluation = Evaluation(
        candidate_id=candidate.id,
        job_id=job.id if job else None,
        created_by=user.id,
        match_score=match["match_score"] if match else None,
        missing_skills=match["missing_skills"] if match else [],
        strengths=match["strengths"] if match else [],
        weaknesses=match["weaknesses"] if match else [],
        summary="\n".join(summary.values()),
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    db.add(Summary(evaluation_id=evaluation.id, **summary))
    db.commit()
    return evaluation, summary
