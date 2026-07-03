from sqlalchemy.orm import Session
from app.ai.interview_generator import generate_interview_questions
from app.models.evaluation import Evaluation
from app.models.interview import Interview
from app.models.user import User
from app.services.candidate_service import get_candidate_or_404
from app.services.job_service import get_job_or_404


def create_interview_questions(db: Session, candidate_id: int, job_id: int, user: User) -> dict:
    candidate = get_candidate_or_404(db, candidate_id)
    job = get_job_or_404(db, job_id)
    questions = generate_interview_questions(candidate, job)
    evaluation = Evaluation(candidate_id=candidate.id, job_id=job.id, created_by=user.id, interview_questions=questions)
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)
    db.add(Interview(evaluation_id=evaluation.id, questions=questions))
    db.commit()
    return {"evaluation_id": evaluation.id, **questions}
