from pathlib import Path
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.candidate import Candidate
from app.models.user import User, UserRole
from app.schemas.candidate import CandidateDetail, CandidateRead
from app.services.embeddings import cosine_similarity, local_embedding
from app.services.resume_parser import extract_profile, save_and_parse_resume


router = APIRouter(prefix="/candidates", tags=["candidates"])


@router.post("/upload", response_model=CandidateRead)
async def upload_candidate(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(require_roles(UserRole.HR)),
):
    path, text = await save_and_parse_resume(file, Path(get_settings().uploads_dir))
    profile = extract_profile(text)
    candidate = Candidate(**profile, resume_file_path=path, created_by=user.id)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    return candidate


@router.get("", response_model=list[CandidateRead])
def list_candidates(
    q: str | None = Query(default=None),
    skill: str | None = Query(default=None),
    semantic: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    query = db.query(Candidate)
    if q:
        query = query.filter(or_(Candidate.name.ilike(f"%{q}%"), Candidate.email.ilike(f"%{q}%")))
    candidates = query.order_by(Candidate.created_at.desc()).all()
    if skill:
        skill_l = skill.lower()
        candidates = [candidate for candidate in candidates if skill_l in {s.lower() for s in candidate.skills}]
    if semantic:
        target = local_embedding(semantic)
        candidates.sort(key=lambda c: cosine_similarity(c.embedding, target), reverse=True)
    return candidates


@router.get("/{candidate_id}", response_model=CandidateDetail)
def get_candidate(candidate_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.delete("/{candidate_id}")
def delete_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(UserRole.HR)),
):
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(candidate)
    db.commit()
    return {"message": "Candidate deleted"}
