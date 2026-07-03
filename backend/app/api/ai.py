from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.candidate import Candidate
from app.models.evaluation import Evaluation
from app.models.job import JobDescription
from app.models.user import User
from app.schemas.ai import EvaluationRead, MatchRequest, MatchResponse, QuestionsRequest, QuestionsResponse, SummaryRequest, SummaryResponse
from app.services.ai_service import generate_questions, match_candidate, summarize_candidate


router = APIRouter(prefix="/ai", tags=["ai"])


def _candidate_job(db: Session, candidate_id: int, job_id: int | None = None):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    job = db.get(JobDescription, job_id) if job_id else None
    if job_id and not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    return candidate, job


@router.post("/match", response_model=MatchResponse)
def match(payload: MatchRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    candidate, job = _candidate_job(db, payload.candidate_id, payload.job_id)
    result = match_candidate(candidate, job)
    evaluation = Evaluation(candidate_id=candidate.id, job_id=job.id, created_by=user.id, **result)
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return MatchResponse(evaluation_id=evaluation.id, candidate_id=candidate.id, job_id=job.id, **result)


@router.post("/questions", response_model=QuestionsResponse)
def questions(payload: QuestionsRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    candidate, job = _candidate_job(db, payload.candidate_id, payload.job_id)
    generated = generate_questions(candidate, job)
    evaluation = Evaluation(candidate_id=candidate.id, job_id=job.id, created_by=user.id, interview_questions=generated)
    db.add(evaluation)
    db.commit()
    return generated


@router.post("/summary", response_model=SummaryResponse)
def summary(payload: SummaryRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    candidate, job = _candidate_job(db, payload.candidate_id, payload.job_id)
    match = match_candidate(candidate, job) if job else None
    generated = summarize_candidate(candidate, job, match)
    evaluation = Evaluation(
        candidate_id=candidate.id,
        job_id=job.id if job else None,
        created_by=user.id,
        match_score=match["match_score"] if match else None,
        missing_skills=match["missing_skills"] if match else [],
        strengths=match["strengths"] if match else [],
        weaknesses=match["weaknesses"] if match else [],
        summary="\n".join(generated.values()),
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    return SummaryResponse(evaluation_id=evaluation.id, **generated)


@router.get("/evaluations", response_model=list[EvaluationRead])
def evaluations(candidate_id: int | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Evaluation)
    if candidate_id:
        query = query.filter(Evaluation.candidate_id == candidate_id)
    return query.order_by(Evaluation.created_at.desc()).all()
