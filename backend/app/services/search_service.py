from sqlalchemy.orm import Session
from app.ai.embeddings import cosine_similarity, local_embedding
from app.models.candidate import Candidate
from app.services.candidate_service import list_candidates


def search_candidates(db: Session, q: str | None = None, skill: str | None = None, semantic: str | None = None) -> list[Candidate]:
    candidates = list_candidates(db, q)
    if skill:
        skill_l = skill.lower()
        candidates = [candidate for candidate in candidates if skill_l in {s.lower() for s in candidate.skills}]
    if semantic:
        target = local_embedding(semantic)
        candidates.sort(key=lambda c: cosine_similarity(c.embedding, target), reverse=True)
    return candidates
