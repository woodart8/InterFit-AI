from fastapi import APIRouter

from app.schemas.interview import (
    InterviewStartRequest,
    InterviewStartResponse,
    InterviewAnswerRequest,
    InterviewAnswerResponse,
    InterviewQuestion,
    GenerateFollowUpQuestionRequest,
)

from app.services.interview_service import (
    start_interview,
    submit_answer,
    generate_follow_up_question,
    generate_new_question,
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


@router.post(
    "/{interview_id}/questions/follow-up",
    response_model=InterviewQuestion,
)
async def generate_follow_up_question_api(
    interview_id: str,
    request: GenerateFollowUpQuestionRequest,
):
    return generate_follow_up_question(
        interview_id=interview_id,
        question_id=request.question_id,
    )


@router.post(
    "/{interview_id}/questions/new",
    response_model=InterviewQuestion,
)
async def generate_new_question_api(
    interview_id: str,
):
    return generate_new_question(
        interview_id=interview_id,
    )