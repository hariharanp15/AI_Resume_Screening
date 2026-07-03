from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.ai.embeddings import local_embedding
from app.models.job import JobDescription
from app.models.user import User
from app.schemas.job import JobCreate, JobUpdate


def create_job(db: Session, payload: JobCreate, user: User) -> JobDescription:
    job = JobDescription(**payload.model_dump(), embedding=local_embedding(payload.content), created_by=user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def list_jobs(db: Session) -> list[JobDescription]:
    return db.query(JobDescription).order_by(JobDescription.created_at.desc()).all()


def get_job_or_404(db: Session, job_id: int) -> JobDescription:
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    return job


def update_job(db: Session, job_id: int, payload: JobUpdate) -> JobDescription:
    job = get_job_or_404(db, job_id)
    for key, value in payload.model_dump().items():
        setattr(job, key, value)
    job.embedding = local_embedding(payload.content)
    db.commit()
    db.refresh(job)
    return job


def delete_job(db: Session, job_id: int) -> None:
    db.delete(get_job_or_404(db, job_id))
    db.commit()
