from collections import Counter
from sqlalchemy.orm import Session
from app.models.candidate import Candidate
from app.models.evaluation import Evaluation
from app.models.job import JobDescription


def get_analytics(db: Session) -> dict:
    candidates = db.query(Candidate).all()
    jobs = db.query(JobDescription).all()
    scores = [
        row.match_score
        for row in db.query(Evaluation).filter(Evaluation.match_score.is_not(None)).all()
        if row.match_score is not None
    ]
    skill_counts = Counter(
        skill.strip()
        for job in jobs
        for skill in (job.required_skills or [])
        if skill and skill.strip()
    )
    return {
        "total_candidates": len(candidates),
        "total_job_descriptions": len(jobs),
        "average_match_score": round(sum(scores) / len(scores), 2) if scores else 0.0,
        "most_requested_skills": [
            {"skill": skill, "count": count}
            for skill, count in skill_counts.most_common(8)
        ],
        "recent_candidate_uploads": [
            {"id": candidate.id, "name": candidate.name, "created_at": candidate.created_at.isoformat()}
            for candidate in sorted(candidates, key=lambda item: item.created_at, reverse=True)[:5]
        ],
        "most_active_users": [],
    }
