from datetime import datetime
from pydantic import BaseModel


class MatchRequest(BaseModel):
    candidate_id: int
    job_id: int


class QuestionsRequest(BaseModel):
    candidate_id: int
    job_id: int


class SummaryRequest(BaseModel):
    candidate_id: int
    job_id: int | None = None


class QuestionsResponse(BaseModel):
    technical: list[str]
    scenario_based: list[str]
    behavioral: list[str]


class MatchResponse(BaseModel):
    evaluation_id: int
    candidate_id: int
    job_id: int
    match_score: float
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]


class SummaryResponse(BaseModel):
    evaluation_id: int
    overview: str
    skill_assessment: str
    experience_summary: str
    hiring_recommendation: str


class EvaluationRead(BaseModel):
    id: int
    candidate_id: int
    job_id: int | None
    match_score: float | None
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    summary: str | None
    interview_questions: dict
    created_at: datetime

    class Config:
        from_attributes = True
