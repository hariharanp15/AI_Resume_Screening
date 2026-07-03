from fastapi import HTTPException, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.ai.parser import extract_resume_profile
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.user import User
from app.schemas.candidate import CandidateUpdate
from app.services.resume_service import save_and_extract_resume


async def upload_candidate_resume(db: Session, file: UploadFile, user: User) -> Candidate:
    path, text = await save_and_extract_resume(file)
    profile = extract_resume_profile(text)
    candidate = Candidate(**profile, resume_file_path=str(path), created_by=user.id)
    db.add(candidate)
    db.commit()
    db.refresh(candidate)
    db.add(Resume(candidate_id=candidate.id, file_name=file.filename or "resume", file_path=str(path), extracted_text=text))
    db.commit()
    db.refresh(candidate)
    return candidate


def list_candidates(db: Session, q: str | None = None) -> list[Candidate]:
    query = db.query(Candidate)
    if q:
        query = query.filter(or_(Candidate.name.ilike(f"%{q}%"), Candidate.email.ilike(f"%{q}%")))
    return query.order_by(Candidate.created_at.desc()).all()


def get_candidate_or_404(db: Session, candidate_id: int) -> Candidate:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


def delete_candidate(db: Session, candidate_id: int) -> None:
    candidate = get_candidate_or_404(db, candidate_id)
    db.delete(candidate)
    db.commit()


def update_candidate(db: Session, candidate_id: int, payload: CandidateUpdate) -> Candidate:
    candidate = get_candidate_or_404(db, candidate_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(candidate, key, value)
    db.commit()
    db.refresh(candidate)
    return candidate
