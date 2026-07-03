from sqlalchemy.orm import Session
from app.ai.interview_generator import generate_interview_questions
from app.ai.matcher import match_candidate_to_job
from app.ai.summary_generator import generate_candidate_summary
from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.summary import Summary
from app.models.user import User
from app.services.candidate_service import get_candidate_or_404
from app.services.job_service import get_job_or_404


def create_match_evaluation(db: Session, candidate_id: int, job_id: int, user: User) -> tuple[Evaluation, dict]:
    candidate = get_candidate_or_404(db, candidate_id)
    job = get_job_or_404(db, job_id)
    result = match_candidate_to_job(candidate, job)
    evaluation = Evaluation(candidate_id=candidate.id, job_id=job.id, created_by=user.id, **result)
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return evaluation, result


def create_full_evaluation(db: Session, candidate_id: int, job_id: int, user: User) -> tuple[Evaluation, dict]:
    candidate = get_candidate_or_404(db, candidate_id)
    job = get_job_or_404(db, job_id)
    match = match_candidate_to_job(candidate, job)
    questions = generate_interview_questions(candidate, job)
    summary = generate_candidate_summary(candidate, job, match)
    evaluation = Evaluation(
        candidate_id=candidate.id,
        job_id=job.id,
        created_by=user.id,
        match_score=match["match_score"],
        missing_skills=match["missing_skills"],
        strengths=match["strengths"],
        weaknesses=match["weaknesses"],
        interview_questions=questions,
        summary="\n".join(summary.values()),
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    db.add(Interview(evaluation_id=evaluation.id, questions=questions))
    db.add(Summary(evaluation_id=evaluation.id, **summary))
    db.commit()
    return evaluation, {**match, "questions": questions, "summary": summary}
