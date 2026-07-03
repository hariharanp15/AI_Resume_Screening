from datetime import datetime
from pydantic import BaseModel
from app.schemas.interview import QuestionAnswer


class MatchRequest(BaseModel):
    candidate_id: int
    job_id: int


class MatchResponse(BaseModel):
    evaluation_id: int
    candidate_id: int
    job_id: int
    match_score: float
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]


class EvaluationRead(BaseModel):
    id: int
    candidate_id: int
    candidate_name: str | None = None
    job_id: int | None
    job_title: str | None = None
    match_score: float | None
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    summary: str | None
    interview_questions: dict
    created_at: datetime

class EvaluationHistoryRead(BaseModel):
    id: int
    candidate_id: int
    candidate_name: str
    job_id: int | None
    job_title: str | None
    match_score: float | None
    missing_skills: list[str] = []
    strengths: list[str] = []
    weaknesses: list[str] = []
    summary: str | None = None
    interview_questions: dict = {}
    created_at: datetime


class FullEvaluationResponse(BaseModel):
    evaluation_id: int
    candidate_id: int
    job_id: int
    match_score: float
    missing_skills: list[str]
    strengths: list[str]
    weaknesses: list[str]
    questions: dict[str, list[QuestionAnswer]]
    summary: dict[str, str]
