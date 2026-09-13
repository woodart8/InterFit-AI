from pydantic import BaseModel


class InterviewStartRequest(BaseModel):
    resume_id: str


class InterviewQuestion(BaseModel):
    id: str
    content: str


class InterviewStartResponse(BaseModel):
    interview_id: str
    question: InterviewQuestion


class InterviewAnswerRequest(BaseModel):
    question_id: str
    answer: str


class InterviewAnswerResponse(BaseModel):
    interview_id: str
    question_id: str


class GenerateFollowUpQuestionRequest(BaseModel):
    question_id: str
