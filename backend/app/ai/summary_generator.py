from app.models.candidate import Candidate
from app.models.job import JobDescription


def generate_candidate_summary(candidate: Candidate, job: JobDescription | None = None, match: dict | None = None) -> dict:
    if not candidate.resume_text or len(candidate.resume_text.strip()) < 80:
        return {
            "overview": "Insufficient information is available to generate a reliable candidate summary.",
            "skill_assessment": "Not enough resume content was extracted.",
            "experience_summary": "Experience details are unavailable.",
            "hiring_recommendation": "Request a clearer resume before making a decision.",
        }
    role_context = f" for {job.title}" if job else ""
    score = match.get("match_score") if match else None
    recommendation = "Strongly shortlist" if score and score >= 75 else "Consider with skill-gap review" if score and score >= 55 else "Do not shortlist yet"
    return {
        "overview": f"{candidate.name} appears to be a candidate{role_context} with skills in {', '.join(candidate.skills[:8]) or 'areas not clearly extracted'}.",
        "skill_assessment": f"Key extracted skills: {', '.join(candidate.skills) or 'None detected'}.",
        "experience_summary": candidate.work_experience or "The resume does not provide enough structured experience detail.",
        "hiring_recommendation": recommendation,
    }
