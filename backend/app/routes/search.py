from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.config.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.candidate import CandidateRead
from app.services.search_service import search_candidates


router = APIRouter(prefix="/search", tags=["search"])


@router.get("/candidates", response_model=list[CandidateRead])
def search_candidate_route(
    q: str | None = Query(default=None),
    skill: str | None = Query(default=None),
    semantic: str | None = Query(default=None),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
):
    return search_candidates(db, q=q, skill=skill, semantic=semantic)
