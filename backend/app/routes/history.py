from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.evaluation import Evaluation
from app.models.user import User
from app.schemas.evaluation import EvaluationHistoryRead


router = APIRouter(prefix="/history", tags=["history"])


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


@router.delete("/evaluations/{evaluation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_evaluation(evaluation_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    evaluation = db.get(Evaluation, evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Evaluation not found")
    db.delete(evaluation)
    db.commit()
