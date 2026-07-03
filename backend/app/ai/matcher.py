from app.ai.embeddings import cosine_similarity
from app.models.candidate import Candidate
from app.models.job import JobDescription


def normalize_skill_set(skills: list[str]) -> set[str]:
    return {skill.strip().lower() for skill in skills if skill.strip()}


def match_candidate_to_job(candidate: Candidate, job: JobDescription) -> dict:
    candidate_skills = normalize_skill_set(candidate.skills)
    required_skills = normalize_skill_set(job.required_skills)
    matched = sorted(candidate_skills & required_skills)
    missing = sorted(required_skills - candidate_skills)
    skill_score = len(matched) / max(len(required_skills), 1)
    semantic_score = cosine_similarity(candidate.embedding, job.embedding)
    score = round((skill_score * 0.7 + semantic_score * 0.3) * 100, 2)
    strengths = [f"Matches required skill: {skill}" for skill in matched[:8]]
    if candidate.work_experience:
        strengths.append("Resume includes relevant work experience signals")
    weaknesses = [f"Missing required skill: {skill}" for skill in missing[:8]]
    if score < 50:
        weaknesses.append("Overall alignment is below the recommended shortlist threshold")
    return {
        "match_score": score,
        "missing_skills": missing,
        "strengths": strengths or ["Profile has partial semantic alignment with the role"],
        "weaknesses": weaknesses or ["No major required skill gaps detected"],
    }
