from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

from app.api import health, resume, interview

app = FastAPI(
    title="InterFit AI",
    description="AI 기반 개인화 면접 서비스",
    version="0.1.0",
)

app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(resume.router, prefix="/api/resumes", tags=["Resume"])
app.include_router(interview.router, prefix="/api/interviews", tags=["Interview"])