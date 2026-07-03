from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.job import JobDescription
from app.models.user import User, UserRole
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.embeddings import local_embedding


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead)
def create_job(payload: JobCreate, db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.HR))):
    job = JobDescription(**payload.model_dump(), embedding=local_embedding(payload.content), created_by=user.id)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("", response_model=list[JobRead])
def list_jobs(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(JobDescription).order_by(JobDescription.created_at.desc()).all()


@router.put("/{job_id}", response_model=JobRead)
def update_job(job_id: int, payload: JobUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    for key, value in payload.model_dump().items():
        setattr(job, key, value)
    job.embedding = local_embedding(payload.content)
    db.commit()
    db.refresh(job)
    return job


@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job description not found")
    db.delete(job)
    db.commit()
    return {"message": "Job description deleted"}
