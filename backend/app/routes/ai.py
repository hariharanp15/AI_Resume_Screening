from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.evaluation import Evaluation
from app.models.user import User
from app.schemas.evaluation import EvaluationHistoryRead, FullEvaluationResponse, MatchRequest, MatchResponse
from app.schemas.interview import QuestionsRequest, QuestionsResponse
from app.schemas.summary import SummaryRequest, SummaryResponse
from app.services.ai_service import create_full_evaluation, create_match_evaluation
from app.services.interview_service import create_interview_questions
from app.services.summary_service import create_candidate_summary


router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/match", response_model=MatchResponse)
def match(payload: MatchRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    evaluation, result = create_match_evaluation(db, payload.candidate_id, payload.job_id, user)
    return MatchResponse(evaluation_id=evaluation.id, candidate_id=payload.candidate_id, job_id=payload.job_id, **result)


@router.post("/evaluate", response_model=FullEvaluationResponse)
def evaluate(payload: MatchRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    evaluation, result = create_full_evaluation(db, payload.candidate_id, payload.job_id, user)
    return FullEvaluationResponse(
        evaluation_id=evaluation.id,
        candidate_id=payload.candidate_id,
        job_id=payload.job_id,
        **result,
    )


@router.post("/questions", response_model=QuestionsResponse)
def questions(payload: QuestionsRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_interview_questions(db, payload.candidate_id, payload.job_id, user)


@router.post("/summary", response_model=SummaryResponse)
def summary(payload: SummaryRequest, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    evaluation, generated = create_candidate_summary(db, payload.candidate_id, payload.job_id, user)
    return SummaryResponse(evaluation_id=evaluation.id, **generated)


@router.get("/evaluations", response_model=list[EvaluationHistoryRead])
def evaluations(candidate_id: int | None = None, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    query = db.query(Evaluation)
    if candidate_id:
        query = query.filter(Evaluation.candidate_id == candidate_id)
    rows = query.order_by(Evaluation.created_at.desc()).all()
    return [
        {
            "id": row.id,
            "candidate_id": row.candidate_id,
            "candidate_name": row.candidate.name if row.candidate else "Unknown Candidate",
            "job_id": row.job_id,
            "job_title": row.job.title if row.job else None,
            "match_score": row.match_score,
            "missing_skills": row.missing_skills or [],
            "strengths": row.strengths or [],
            "weaknesses": row.weaknesses or [],
            "summary": row.summary,
            "interview_questions": row.interview_questions or {},
            "created_at": row.created_at,
        }
        for row in rows
    ]
