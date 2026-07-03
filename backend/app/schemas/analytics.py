from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_candidates: int
    total_job_descriptions: int
    average_match_score: float
    most_requested_skills: list[dict]
    recent_candidate_uploads: list[dict]
    most_active_users: list[dict]
