from pydantic import BaseModel


class QuestionsRequest(BaseModel):
    candidate_id: int
    job_id: int


class QuestionAnswer(BaseModel):
    question: str
    answer: str


class QuestionsResponse(BaseModel):
    evaluation_id: int | None = None
    technical: list[QuestionAnswer]
    scenario_based: list[QuestionAnswer]
    behavioral: list[QuestionAnswer]
