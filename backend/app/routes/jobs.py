from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.role import UserRole
from app.models.user import User
from app.schemas.job import JobCreate, JobRead, JobUpdate
from app.services.job_service import create_job, delete_job, list_jobs, update_job


router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.post("", response_model=JobRead)
def create_job_route(payload: JobCreate, db: Session = Depends(get_db), user: User = Depends(require_roles(UserRole.HR))):
    return create_job(db, payload, user)


@router.get("", response_model=list[JobRead])
def list_job_route(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return list_jobs(db)


@router.put("/{job_id}", response_model=JobRead)
def update_job_route(job_id: int, payload: JobUpdate, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    return update_job(db, job_id, payload)


@router.delete("/{job_id}")
def delete_job_route(job_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    delete_job(db, job_id)
    return {"message": "Job description deleted"}
