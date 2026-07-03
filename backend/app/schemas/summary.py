from pydantic import BaseModel


class SummaryRequest(BaseModel):
    candidate_id: int
    job_id: int | None = None


class SummaryResponse(BaseModel):
    evaluation_id: int
    overview: str
    skill_assessment: str
    experience_summary: str
    hiring_recommendation: str
