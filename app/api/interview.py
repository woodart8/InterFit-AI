from fastapi import APIRouter

from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
)

from app.services.interview_service import (
    start_interview,
    submit_answer,
)


router = APIRouter()


@router.post(
    "",
    response_model=InterviewStartResponse,
)
async def start_interview_api(
    request: InterviewStartRequest,
):
    return start_interview(request)


@router.post(
    "/{interview_id}/answer",
    response_model=InterviewAnswerResponse,
)
async def submit_answer_api(
    interview_id: str,
    request: InterviewAnswerRequest,
):
    return submit_answer(
        interview_id=interview_id,
        request=request,
    )