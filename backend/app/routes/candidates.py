from fastapi import APIRouter, Depends, File, Query, UploadFile
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_roles
from app.models.role import UserRole
from app.models.user import User
from app.schemas.candidate import CandidateDetail, CandidateRead, CandidateUpdate
from app.services.candidate_service import delete_candidate, get_candidate_or_404, update_candidate, upload_candidate_resume
from app.services.search_service import search_candidates


router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/upload", response_model=CandidateRead)
async def upload_candidate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.HR)),
):
    return await upload_candidate_resume(db, file, user)


@router.get("", response_model=list[CandidateRead])
def list_candidate_route(
    q: str | None = Query(default=None),
    skill: str | None = Query(default=None),
    semantic: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return search_candidates(db, q=q, skill=skill, semantic=semantic)


@router.get("/{candidate_id}", response_model=CandidateDetail)
def get_candidate(candidate_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_candidate_or_404(db, candidate_id)


@router.put("/{candidate_id}", response_model=CandidateRead)
def update_candidate_route(
    candidate_id: int,
    payload: CandidateUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.HR)),
):
    return update_candidate(db, candidate_id, payload)


@router.delete("/{candidate_id}")
def delete_candidate_route(candidate_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.HR))):
    delete_candidate(db, candidate_id)
    return {"message": "Candidate deleted"}
